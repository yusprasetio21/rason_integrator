import json
from dscommon.log import LOG, log_init
from decouple import config
import os
import time
import subprocess
import random
import mqexchange
from datetime import datetime, timezone
import re

log_init(fpath='/var/log/rasonintegrator/ftp-receiver.log')
mqexchange.init_mq()

def archive_data(file_path, target):
    try:
        # shutil.move(file_path, config('FTP_ARCH_DIR')) # bugs, even root cannot replace files for diff user
        command = f"mv -f '{file_path}' '{target}'"
        result = subprocess.check_output(command, shell=True, text=True)
        log_data = {
            "event": "Move file to archive folder",
            "command": command,
            "result": result
        }
        LOG.info(json.dumps(log_data))
    except subprocess.CalledProcessError as e:
        log_data = {
            "event": "Fail to move file to archive folder",
            "error": str(e)
        }
        LOG.error(json.dumps(log_data))
    except Exception as e:
        log_data = {
            "event": "Fail to move file to archive folder",
            "error": str(e)
        }
        LOG.error(json.dumps(log_data))

def move_data(file_path, target):
    try:
        command = f"mv -f '{file_path}' '{target}'"
        result = subprocess.check_output(command, shell=True, text=True)
        log_data = {
            "event": "Move file to forwarder folder",
            "command": command,
            "result": result
        }
        LOG.info(json.dumps(log_data))
    except subprocess.CalledProcessError as e:
        log_data = {
            "event": "Fail to move file to forwarder folder",
            "error": str(e)
        }
        LOG.error(json.dumps(log_data))
        raise e
    except Exception as e:
        log_data = {
            "event": "Fail to move file to forwarder folder",
            "error": str(e)
        }
        LOG.error(json.dumps(log_data))
        raise e

def copy_data(file_path, target):
    try:
        command = f"cp -f '{file_path}' '{target}'"
        result = subprocess.check_output(command, shell=True, text=True)
        log_data = {
            "event": "Copy file to forwarder folder",
            "command": command,
            "result": result
        }
        LOG.info(json.dumps(log_data))
    except subprocess.CalledProcessError as e:
        log_data = {
            "event": "Fail to Copy file to forwarder folder",
            "error": str(e)
        }
        LOG.error(json.dumps(log_data))
        raise e
    except Exception as e:
        log_data = {
            "event": "Fail to Copy file to forwarder folder",
            "error": str(e)
        }
        LOG.error(json.dumps(log_data))
        raise e
    
def read_file_as_string(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except Exception as e:
        log_data = { "event": "Fail to read rason file", "error": str(e) }
        LOG.error(json.dumps(log_data))
        raise e
              
def scan_folder_and_send(path, done_path, target_path, error_path):
    # List all files in the directory
    fn_list = os.listdir(path)
    random.shuffle(fn_list)  # Agar multi worker tidak berebut file
    for filename in fn_list:
        if not filename.endswith('.tmp'): 
            log_data = {"event": "Scan ftp", "filename": filename}
            
            try:
                rel_file_path = os.path.join(path, filename)
                
                # Cek ekstensi file
                _, ext = os.path.splitext(filename)  # ext termasuk titik, misal '.DAT', '.X'
                allowed_exts = ['.DAT', '.X', '.a', '.A']  # '' artinya tanpa ekstensi
                
                if ext.upper() in allowed_exts:
                    # Perubahan: Jika file ASCII dan berakhiran .dat, ubah ekstensi ke .X
                    if filename.lower().endswith('.dat'):
                        log_data["note"] = "Ekstensi .DAT diubah menjadi .X"

                        x_filename = filename[:-4] + '.X'
                        x_rel_file_path = os.path.join(path, x_filename)
                        os.rename(rel_file_path, x_rel_file_path)

                        # Replace old fn
                        rel_file_path = x_rel_file_path
                        filename = x_filename
                        LOG.info(json.dumps(log_data))
                    
                     # Perubahan: Jika file ASCII dan berakhiran .a, ubah ekstensi ke .X
                    if filename.lower().endswith('.a'):
                        log_data["note"] = "Ekstensi .a diubah menjadi .X"

                        x_filename = filename[:-2] + '.X'
                        x_rel_file_path = os.path.join(path, x_filename)
                        os.rename(rel_file_path, x_rel_file_path)

                        # Replace old fn
                        rel_file_path = x_rel_file_path
                        filename = x_filename
                        LOG.info(json.dumps(log_data))
                    
                    content = read_file_as_string(rel_file_path)
                    if content is None:
                        raise Exception("Empty rason file")

                    # Split sandi
                    blocks = []
                    for part in content.split('='):
                        # Remove NNNN or NNNNN with any surrounding whitespace/newlines
                        cleaned = re.sub(r'\s*NNNNN?\s*', ' ', part).strip()
                        
                        # check bad vendor data
                        cleaned = get_data_with_valid_header(cleaned)
                        if cleaned:  
                            blocks.append(cleaned + '=')
                    
                    if len(blocks) == 0:
                        raise Exception('Empty blocks')
                    
                    # Proses sandi
                    # Kirim setiap blok ke RabbitMQ
                    for idx, block in enumerate(blocks):
                        body_q = {
                            "message": block,
                            "recv_timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S'),
                            "block_index": idx + 1,
                            "source_file": filename
                        }
                        status_mq = mqexchange.publish_message(json.dumps(body_q))
                        block_log_data = {"event": "Rabbitmq publish", "block_index": idx + 1, "body": body_q}
                        if not status_mq:
                            block_log_data["error"] = f"publish queue gagal pada blok ke-{idx + 1}"
                            LOG.error(json.dumps(block_log_data))
                            raise Exception(block_log_data["error"])
                        LOG.info(json.dumps(block_log_data))

                    # Kirim juga setiap blok ke target folder sebagai file terpisah
                    for idx, block in enumerate(blocks):
                        # Determine block name form header sandi to make debug easier
                        block_name = ""
                        try:
                            block_name = block[:6].replace(' ', '')
                        except:
                            block_name = f"block{idx+1}"
                        
                        # Block file prep.
                        block_filename = f"{filename.split('.')[0]}_{block_name}.X.tmp2"
                        temp_target_file_path = os.path.join(target_path, f"ascii/{block_filename}")

                        # Simpan isi block ke file sementara
                        with open(temp_target_file_path, 'w', encoding='utf-8') as f:
                            f.write(block)

                        # Rename agar siap di-forward
                        final_target_file_path = temp_target_file_path.replace('.tmp2', '.tmp')
                        move_data(temp_target_file_path, final_target_file_path)
                    
                    log_data["status"] = 'Success'
                    LOG.info(json.dumps(log_data))

                    ### THIS CODE IS FOR SENDING SINGLE SANDI FILE
                    # # Temporary file so it wont corrupted by inaswitch forwarder
                    # temp_target_file_path = os.path.join(target_path, f"ascii/{filename}.tmp2")

                    # # Copy file ke rason forwarder sementara
                    # copy_data(rel_file_path, temp_target_file_path)

                    # # Rename dengan .X.tmp sebagai tanda siap di forward
                    # final_target_file_path = os.path.join(target_path, f"ascii/{filename}.tmp")
                    # move_data(temp_target_file_path, final_target_file_path)

                    # log_data["status"] = 'Success'
                    # LOG.info(json.dumps(log_data))
                else:
                    # File dianggap binary, tidak diproses isinya
                    log_data["note"] = "File dianggap binary, tidak dibaca, langsung copy & rename"

                    # Copy file ke rason forwarder sementara
                    temp_target_file_path = os.path.join(target_path, f"binary/{filename}.tmp2")
                    copy_data(rel_file_path, temp_target_file_path)

                    # Rename dengan .bin.tmp sebagai tanda siap forward
                    final_target_file_path = os.path.join(target_path, f"binary/{filename}.tmp")
                    move_data(temp_target_file_path, final_target_file_path)

                    log_data["status"] = 'Success'
                    LOG.info(json.dumps(log_data))

                # Jika archive gagal maka tidak akan terkirim kembali karena ekstensi sudah direname
                new_rel_file_path = os.path.join(done_path, filename)
                archive_data(rel_file_path, new_rel_file_path)

            except Exception as e:
                log_data["status"] = 'Fail'
                log_data["error"] = str(e)
                LOG.error(json.dumps(log_data))

                # Pindahkan file .DAT / .X yang error ke folder error
                _, ext = os.path.splitext(filename)
                if ext.upper() in allowed_exts:
                    try:
                        error_file_path = os.path.join(error_path, filename)
                        archive_data(rel_file_path, error_file_path)
                    except Exception as err_archive:
                        log_data = {
                            "event": "Fail to move file to error folder",
                            "filename": filename,
                            "error": str(err_archive)
                        }
                        LOG.error(json.dumps(log_data))

def get_data_with_valid_header(data):
    if data is None:
        return None
    
    # Normalize line endings: remove all carriage returns (\r),
    # data degrean double CR
    data = re.sub(r'\r+', '\n', data)
    # Collapse multiple blank lines
    data = re.sub(r'\n+', '\n', data)

    pattern = r'^[A-Z]{4}\d{2}\s[A-Z]{4}\s\d{6}(?:\s[A-Z]{3})?$'
    data_line = data.splitlines()

    for i, line in enumerate(data_line):
        line = line.strip()
        if re.match(pattern, line):
            data_line[i] = line
            # result = "\n".join(data_line[i:])
            result = "\n".join(l for l in data_line[i:] if l.strip())
            if i != 0:
                log_data = {
                    "event": "Correcting data",
                    "data": result,
                    "note": "Data diubah karena header tidak valid"
                }
                LOG.info(json.dumps(log_data))
            return result
    return None

if __name__ == "__main__":
    sourcer_base_path = config('SOURCE_DIR')
    received_path = f'{sourcer_base_path}/received/'
    done_path = f'{sourcer_base_path}/sent/'
    error_path = f'{sourcer_base_path}/error/'

    target_base_path = config('TARGET_DIR')
    forward_path = f'{target_base_path}/created/'

    try:
        while True:
            scan_folder_and_send(received_path, done_path, forward_path, error_path)
            time.sleep(2)
    except KeyboardInterrupt:
        log_data = { "event": "Interrupted by user. Closing scanning ftp receive." }
        LOG.info(json.dumps(log_data))
    except Exception as e:
        log_data = { "event": "Fatal main function error", "error": str(e) }
        LOG.error(json.dumps(log_data))
    finally:
        log_data = { "event": "FTP Receiver closed" }
        LOG.info(log_data)