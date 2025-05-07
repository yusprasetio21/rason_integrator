import json
from decouple import config
import subprocess
import time

# Jalankan ketika dua service forwarder running, cek apakah saling error
# jika rebutan biarkan saja asal jangan yang terkirim corrupt
if __name__ == "__main__":
    base_path = config('SOURCE_DIR')
    created_path = f'{base_path}/created/'
    done_path = f'{base_path}/sent/'
    error_path = f'{base_path}/error/'
    target_path = config('FTP_TARGET_DIR')
    
    longstring = "If youre trying to clean up the folder (effectively the files out and deleting them), \
        then you can move the files to a backup or temporary folder, \
            or use rm to delete them if no backup is needed."
    for i in range(100):
        command = f"echo '{longstring}' > {created_path}{i}.X.tmp2"
        result = subprocess.check_output(command, shell=True, text=True)
        
        command = f"mv {created_path}{i}.X.tmp2 {created_path}{i}.X.tmp"
        result = subprocess.check_output(command, shell=True, text=True)