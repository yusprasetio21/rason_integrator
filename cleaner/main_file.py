from decouple import config
from datetime import datetime, timedelta
import time
import pytz
from dscommon.log import LOG, log_init

log_init(fpath='/var/log/rasonintegrator/cleaner.log')

def clean_log_file():
    pass

def clean_data(sekarang):
    # try:
        import tarfile
        import glob
        import os
        import subprocess

        archdir = config('FTP_ARCH_DIR')
        retention = int(config('FILE_RETENTION_DAYS'))
        ts_to_clear = datetime.strftime(sekarang - timedelta(days=retention), "%Y%m%d%H%M")
        ts_to_clear_ts = time.mktime((sekarang - timedelta(days=retention)).timetuple())

        # List of files to include in the archive
        json_files = glob.glob(f"{archdir}/*.X")
        files_to_archive = []
        for json_file in json_files:
            # datedata = os.path.basename(json_file).split("_")[1]
            datedata = os.path.getmtime(json_file)
            if datedata <= ts_to_clear_ts:
                files_to_archive.append(json_file)

        # Name of the output archive file
        output_archive_file = f"{archdir}/archive_before_{ts_to_clear}.tar.gz"

        LOG.info(f"Archiving data for {ts_to_clear}")
        if len(files_to_archive) == 0:
            LOG.info(f"No files to archived")
            return
        
        # Create a `.tar.gz` archive
        count_file_archive = 0
        with tarfile.open(output_archive_file, "w:gz") as tar:
            for file_to_add in files_to_archive:
                # Add each file to the archive
                tar.add(file_to_add)
                count_file_archive += 1
        LOG.info(f"{count_file_archive} files archived on: {output_archive_file}")

        # Remove txt file
        LOG.info(f"Removing data for {ts_to_clear}")
        count_file_rm = 0
        for file_to_add in files_to_archive:
            command = f"rm -f {file_to_add}"
            result = subprocess.check_output(command, shell=True, text=True)
            count_file_rm += 1
        
        LOG.info(f"{count_file_rm} Data Removed")

        # Remove old archive
        LOG.info(f"Removing archive data before {ts_to_clear}")
        tar_files = glob.glob(f"{archdir}/*.tar.gz")
        count_arch_rm = 0
        for tar_file in tar_files:
            datefile = os.path.getmtime(tar_file)
            if datefile <= ts_to_clear_ts:
                command = f"rm -f {tar_file}"
                result = subprocess.check_output(command, shell=True, text=True)
                count_arch_rm += 1

        LOG.info(f"{count_arch_rm} Data Removed")
    # except Exception as e:
    #     LOG.error(f"Fail to archive : {e}")


if __name__ == "__main__":
    LOG.info('Cleaner start')
    sekarang = datetime.now(pytz.UTC)
    clean_data(sekarang)
    LOG.info('Cleaner stop')