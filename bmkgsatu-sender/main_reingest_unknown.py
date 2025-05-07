import json
import uuid
import sys, os
import mqexchange
from dscommon.log import LOG, log_init
from api_gtsmessage import consume_reingest_unknown_gtsmessage

log_init(fpath='/var/log/awosintegrator/bmkgsatu-sender.log')
mqexchange.init_mq()

''' 
should be able to be run in threads
Hanya digunakan ketika banyak antrian di unknown karena metadata salah/tidak ditemukan
'''
def start_sending_gtsmessage():
    mqexchange.consume_unk_message(consume_reingest_unknown_gtsmessage)
    
if __name__ == "__main__":
    # Logging
    uid = str(uuid.uuid4())

    try:
        log_data = { "event": "BMKG Satu sender started", "id": uid }
        LOG.info(json.dumps(log_data))
        
        start_sending_gtsmessage()
    except KeyboardInterrupt:
        log_data = { "event": "BMKG Satu sender stopped", "id": uid }
        LOG.info(json.dumps(log_data))
        
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
            