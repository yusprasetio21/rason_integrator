#!/bin/bash

# Load .env
set -a
source /home/bmkgsatu/rason_integrator/ftp-receiver/.env
set +a

RECEIVED_PATH="${SOURCE_DIR}/received"
SENT_PATH="${SOURCE_DIR}/sent"
TARGET_PATH="${TARGET_DIR}/created"
LOG_FILE="/var/log/rasonintegrator/ftp-receiver.log"

log_info() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] $1" >> "$LOG_FILE"
}

log_error() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] $1" >> "$LOG_FILE"
}

# === Tambahan: Tampilkan dan Log Proses Aktif ===
SCRIPT_NAME=$(basename "$0")

log_info "==== Memulai ftp_receiver.sh ===="
log_info "PID script ini: $$"
log_info "Proses serupa yang sedang berjalan:"

ps -ef | grep "$SCRIPT_NAME" | grep -v grep >> "$LOG_FILE"

log_info "Proses python aktif (jika ada):"
ps -ef | grep 'ftp-receiver' | grep -v grep >> "$LOG_FILE"

echo "==== Proses aktif saat start ===="
ps -ef | grep "$SCRIPT_NAME" | grep -v grep
ps -ef | grep 'ftp-receiver' | grep -v grep
echo "==============================="

# === END Tambahan ===

archive_file() {
  mv -f "$1" "$2" 2>>"$LOG_FILE"
  if [ $? -eq 0 ]; then
    log_info "Archived file $1 to $2"
  else
    log_error "Failed to archive $1"
  fi
}

copy_file() {
  cp -f "$1" "$2" 2>>"$LOG_FILE"
  if [ $? -eq 0 ]; then
    log_info "Copied file $1 to $2"
  else
    log_error "Failed to copy $1"
  fi
}

move_file() {
  mv -f "$1" "$2" 2>>"$LOG_FILE"
  if [ $? -eq 0 ]; then
    log_info "Moved file $1 to $2"
  else
    log_error "Failed to move $1"
  fi
}

process_files() {
  for file in "$RECEIVED_PATH"/*; do
    [ -f "$file" ] || continue
    filename=$(basename "$file")

    if [[ "$filename" == *.* ]]; then
      continue
    fi

    log_info "Processing file $filename"

    content=$(cat "$file")
    if [ -z "$content" ]; then
      log_error "Empty file: $filename"
      continue
    fi

    # --- RabbitMQ publish via curl (Optional - Uncomment if used) ---
    # blocks=$(echo "$content" | awk -v RS='NNNNN' '{gsub(/\n/, "\\n"); print}')
    # for block in $blocks; do
    #   json_payload="{\"message\":\"$block\",\"recv_timestamp\":\"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\",\"source_file\":\"$filename\"}"
    #   curl -u guest:guest -H "Content-Type: application/json" -X POST \
    #     -d "$json_payload" http://172.19.0.202:15672/api/exchanges/%2f/$RABBITMQ_MSGQ/publish >> "$LOG_FILE"
    # done

    temp_target="${TARGET_PATH}/${filename}.X.tmp2"
    final_target="${TARGET_PATH}/${filename}.X.tmp"
    copy_file "$file" "$temp_target"
    move_file "$temp_target" "$final_target"

    archive_file "$file" "${SENT_PATH}/${filename}"
  done
}

while true; do
  process_files
  sleep 2
done
