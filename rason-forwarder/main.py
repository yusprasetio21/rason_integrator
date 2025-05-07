import json
from dscommon.log import LOG, log_init
from decouple import config
import os
import ftplib
from ftplib import FTP
import time
import subprocess
import random

log_init(fpath='/var/log/rasonintegrator/rason-forwarder.log')


def connect_ftp(host, user, password):
    try:
        ftp = FTP(host)
        ftp.login(user=user, passwd=password)

        log_data = {
            "event": "Success to connect to FTP server"
        }
        LOG.info(json.dumps(log_data))

        return ftp
    except Exception as e:
        log_data = {
            "event": "Failed to connect to FTP server",
            "error": str(e)
        }
        LOG.warning(json.dumps(log_data))
        return None


def check_ftp_connection(ftp):
    try:
        ftp.pwd()
        return True
    except Exception:
        return False


def archive_data(file_path, target):
    try:
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


def scan_folder_and_send(ftp, path, done_path, target_path, ftp_mode):
    may_should_reconnect = False

    fn_list = os.listdir(path)
    random.shuffle(fn_list)  # agar multi worker tidak rebutan file
    for filename in fn_list:
        if filename.endswith('.tmp'):
            log_data = {
                "event": "Send ftp",
                "filename": filename
            }

            try:
                rel_file_path = os.path.join(path, filename)

                with open(rel_file_path, 'rb') as file:
                    ftp.storbinary(f'STOR {target_path}/{filename}', file)
                    log_data["ftp_mode"] = ftp_mode

                new_filename = filename.replace('.tmp', '')
                ftp.rename(f'{target_path}/{filename}', f'{target_path}/{new_filename}')

                log_data["status"] = 'Success'
                LOG.info(json.dumps(log_data))

                new_rel_file_path = os.path.join(done_path, new_filename)
                archive_data(rel_file_path, new_rel_file_path)

            except ftplib.error_temp as e:
                if '421' in str(e):
                    log_data["status"] = 'Timeout'
                    log_data["debug"] = str(e)
                    LOG.debug(json.dumps(log_data))
                else:
                    log_data["status"] = 'Fail'
                    log_data["error"] = str(e)
                    LOG.error(json.dumps(log_data))
                return True

            except Exception as e:
                log_data["status"] = 'Fail'
                log_data["error"] = str(e)
                LOG.error(json.dumps(log_data))
                may_should_reconnect = True

    return may_should_reconnect


if __name__ == "__main__":
    base_path = config('SOURCE_DIR')
    created_path = f'{base_path}/created'
    done_path = f'{base_path}/sent'
    error_path = f'{base_path}/error/'
    target_path = config('FTP_TARGET_DIR')
    ftp_mode = config('FTP_MODE', default='binary').lower()
    if ftp_mode == 'binary':
        created_path = f'{created_path}/binary/'
        done_path = f'{done_path}/binary/'
    else:
        created_path = f'{created_path}/ascii/'
        done_path = f'{done_path}/ascii/'

    ftp = connect_ftp(config('FTP_HOST'), config('FTP_USERNAME'), config('FTP_PASSWORD'))

    try:
        while True:
            may_should_reconnect = scan_folder_and_send(ftp, created_path, done_path, target_path, ftp_mode)

            if may_should_reconnect and not check_ftp_connection(ftp):
                try:
                    ftp.quit()
                except:
                    pass

                ftp = connect_ftp(config('FTP_HOST'), config('FTP_USERNAME'), config('FTP_PASSWORD'))
                if ftp is None:
                    time.sleep(7)
                time.sleep(3)
            else:
                time.sleep(1)

    except KeyboardInterrupt:
        log_data = {
            "event": "Interrupted by user. Closing FTP connection."
        }
        LOG.info(json.dumps(log_data))

    except Exception as e:
        log_data = {
            "event": "Fatal main function error",
            "error": str(e)
        }
        LOG.error(json.dumps(log_data))

    finally:
        try:
            ftp.quit()
        except:
            pass

        log_data = {
            "event": "Forwarder closed"
        }
        LOG.info(json.dumps(log_data))
