import requests
from tenacity import retry, wait_fixed, stop_after_attempt
from requests.auth import HTTPBasicAuth
from decouple import config
from datetime import datetime
from dscommon.log import LOG
import json
from requests.exceptions import RequestException
import re
from dscommon.mqhandler import serialize_callback_info
import mqexchange
import time

base_url = config('BMKGSATU_URL')
username = config('BMKGSATU_USER')
password = config('BMKGSATU_PASSWD')

headers = {
    "Content-Type": "application/json"
}

def open_metadata():
    try:
        metadata = None
        with open(f"./{config('META_PATH')}", 'r') as file:
            metadata = json.load(file)
        
        if metadata is None:
            log_data = { "event": "Metadata is broken/empty"}
            LOG.error(json.dumps(log_data))
            return None
        return metadata
    except Exception as e:
          log_data = { "event": "Metadata is broken/empty", "error": str(e)}
          LOG.error(json.dumps(log_data))
          return None
    
def open_header():
    try:
        header = None
        with open(f"./{config('HEADER_PATH')}", 'r') as file:
            header = json.load(file)
        
        if header is None:
            log_data = { "event": "Header is broken/empty"}
            LOG.error(json.dumps(log_data))
            return None
        return header
    except Exception as e:
          log_data = { "event": "Header is broken/empty", "error": str(e)}
          LOG.error(json.dumps(log_data))
          return None

def create_datatimestamp(recv_timestamp, YYGGgg):
    try:
        recv_timestamp_dt = datetime.strptime(recv_timestamp, '%Y-%m-%dT%H:%M:%S')
        timestamp_data_dt = recv_timestamp_dt
        timestamp_data_dt = timestamp_data_dt.replace(day=int(YYGGgg[0:2]), 
                                                    hour=int(YYGGgg[2:4]), 
                                                    minute=int(YYGGgg[4:6]), 
                                                    second=0)
        ## Case khusus
        ## Diterima tanggal 1-10, datetime tgl 28/29/30/31
        if recv_timestamp_dt.day <= 10 and timestamp_data_dt.day >= 28:
            bulan = recv_timestamp_dt.month - 1
            tahun = recv_timestamp_dt.year
            if bulan < 1: # Jika desember
                bulan = 12 
                tahun = recv_timestamp_dt.year - 1
            timestamp_data_dt.replace(month=bulan, year=tahun)
        timestamp_data = timestamp_data_dt.strftime('%Y-%m-%dT%H:%M:%S') 
        return timestamp_data
    except Exception as e:
        log_data = { "event": "create_datatimestamp", "error": str(e)}
        LOG.error(json.dumps(log_data))
        raise

def consume_for_gtsmessage(ch, method, properties, body):
    try:
        log_data = { 
            "event": "BMKG Satu sender consume",
            # **serialize_callback_info(ch, method, properties),
            "body": json.loads(body)
        }
        LOG.info(json.dumps(log_data))
        
        url, data = create_gtsmessage_payload(body)
        if data is not None and data != 'unk':
            response = post_gtsmessage(url, data)
            
            log_data = { 
                "event": "BMKG Satu sender api success", 
                "code": response.status_code,  
                "response": response.json()
            }
            LOG.info(json.dumps(log_data))
            
        if data == 'unk':
            # Unrecognized CCCC will be forwarded into unknown queue
            forward_message_unknown(body)
        
        # Always ack walaupun sandi salah, tapi tdk ack jika gagal kirim
        # saat url invalid harusnya masuk sini juga karena data pasti none
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except requests.exceptions.ConnectionError as e:
        log_data = { "event": "BMKG Satu sender api connection error", "error": str(e) }
        LOG.error(json.dumps(log_data))
        
        time.sleep(5)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True) # akan diganti dengan DLX
    except requests.exceptions.HTTPError as e:
        # Ketelitian ID gts hanya sampai second, potensi id conflict karena burst data
        if e is not None and e.response.status_code == 409:
            log_data = { "event": "BMKG Satu sender api conflict error", "error": str(e) }
            LOG.error(json.dumps(log_data))
            
            time.sleep(1.1) # wait for different id
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        elif e is not None and e.response.status_code == 412:
            log_data = { "event": "BMKG Satu sender api precondition failed", "error": str(e) }
            LOG.error(json.dumps(log_data))
            
            time.sleep(1.1)
            forward_message_unknown(body)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            if e is not None and e.response.status_code >= 400 and e.response.status_code <= 599:
                log_data = { "event": "BMKG Satu sender api other status code", "error": str(e) }
                LOG.error(json.dumps(log_data))
                
                # time.sleep(1.1) # wait, maybe server down
                # ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            else:
                log_data = { "event": "BMKG Satu sender api HTTPError unhandled error", "error": str(e) }
                LOG.error(json.dumps(log_data))
                # ch.basic_ack(delivery_tag=method.delivery_tag)
            
            replay_message_sandi(body)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            time.sleep(2)
    except Exception as e:
        log_data = { "event": "BMKG Satu sender api fatal error", "error": str(e) }
        LOG.error(json.dumps(log_data))
        
        replay_message_sandi(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        time.sleep(2)

def consume_reingest_unknown_gtsmessage(ch, method, properties, body):
    try:
        log_data = { "event": "BMKG Satu sender consume", "body": json.loads(body) }
        LOG.info(json.dumps(log_data))
        
        url, data = create_gtsmessage_payload(body)
        if data is not None and data != 'unk':
            response = post_gtsmessage(url, data)
            
            log_data = { 
                "event": "BMKG Satu sender api success", 
                "code": response.status_code,  
                "response": response.json()
            }
            LOG.info(json.dumps(log_data))
            
        if data == 'unk':
            # Unrecognized CCCC will go to exception
            raise Exception("Station unknown")
        
        # Always ack walaupun sandi salah, tapi tdk ack jika gagal kirim
        # saat url invalid harusnya masuk sini juga karena data pasti none
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    except requests.exceptions.ConnectionError as e:
        log_data = { "event": "BMKG Satu sender api connection error", "error": str(e) }
        LOG.error(json.dumps(log_data))
        
        time.sleep(5)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True) # akan diganti dengan DLX
    except requests.exceptions.HTTPError as e:
        # Ketelitian ID gts hanya sampai second, potensi id conflict karena burst data
        if e is not None and e.response.status_code == 409:
            log_data = { "event": "BMKG Satu sender api conflict error", "error": str(e) }
            LOG.error(json.dumps(log_data))
            
            time.sleep(1.1) # wait for different id
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        else:
            if e is not None and e.response.status_code == 412:
                log_data = { "event": "BMKG Satu sender api precondition failed", "error": str(e) }
                LOG.error(json.dumps(log_data))
            elif e is not None and e.response.status_code >= 400 and e.response.status_code <= 599:
                log_data = { "event": "BMKG Satu sender api other status code", "error": str(e) }
                LOG.error(json.dumps(log_data))
            else:
                log_data = { "event": "BMKG Satu sender api HTTPError unhandled error", "error": str(e) }
                LOG.error(json.dumps(log_data))
        
            # Republish to end of queue
            forward_message_unknown(body)
            ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        log_data = { "event": "BMKG Satu sender api fail", "error": str(e) }
        LOG.error(json.dumps(log_data))
        
        # Republish to end of queue
        forward_message_unknown(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    finally:
        # relax so unknown queue wont bother main queue
        time.sleep(3)
        
def create_gtsmessage_payload(body):
    global base_url
    
    try:
        bodyjs = json.loads(body)
        message = bodyjs["message"]
        recv_timestamp = bodyjs["recv_timestamp"]
        
        ttaaii = message[:6]
        cccc = message[7:11]
        YYGGgg = message[12:18]
        url = None
        
        # should i open every time to update without restart?
        metadata, header_list = open_metadata(), open_header() 
        if metadata is None or header_list is None:
            return None, None
        
        if len(ttaaii) == 6 and len(cccc) == 4 and \
            len(YYGGgg) == 6 and is_valid_header(ttaaii, header_list) and \
            is_four_alpha_characters(cccc) and is_six_digit_number(YYGGgg):

            cccc = cccc.upper()
            
            # Check metadata
            metadata_station = metadata.get(cccc)
            if metadata_station is None:
                log_data = { "event": "Station not recognized", "body": bodyjs }
                LOG.error(json.dumps(log_data))
                return 'unk', 'unk'
                
            wmo_id = metadata_station["wmo_id"]
            url = f"{base_url}{metadata_station['url']}"
            
            timestamp_data = create_datatimestamp(recv_timestamp, YYGGgg)
            
            type_message = get_type_message(ttaaii, header_list)
            if type_message is None:
                log_data = { "event": "Header type message not recognized", "body": bodyjs }
                LOG.error(json.dumps(log_data))
                return 'unk', 'unk'
            
            dt_now = datetime.now().strftime('%Y%m%d%H%M%S')
            idp = f'{type_message}{str(wmo_id)}{dt_now}' # "049999120241103173720"
            
            payload = {
                "@type":"GTSMessage",
                "id":idp,
                "type_message": type_message,
                "sandi_gts": message,
                "timestamp_sent_data": recv_timestamp, # "2024-11-03T17:37:20",
                "timestamp_data": timestamp_data, # "2024-11-01T01:01:00",
                "wmoid": wmo_id,
                "ttaaii": ttaaii,
                "cccc": cccc,
                "need_ftp": 0 # no forward to transmet
            }
            
            log_data = { "event": "Parsing message", "payload": payload }
            LOG.info(json.dumps(log_data))
        
            return url, payload
        
        log_data = { "event": "Parsing message not recognized", "body": bodyjs }
        LOG.error(json.dumps(log_data))
        
        return None, None
    except Exception as e:
        log_data = { "event": "Parsing message fail", "error": str(e) }
        LOG.error(json.dumps(log_data))
        return None, None

def forward_message_unknown(body):
    status_mq = mqexchange.publish_unk_message(body)
    body_j = json.loads(body)
    if status_mq:
        log_data = { "event": "Rabbitmq publish into unknown queue", "body": body_j }
        LOG.info(json.dumps(log_data))
    else:
        log_data = { "event": "Rabbitmq fail publish into unknown queue", "body": body_j }
        LOG.error(json.dumps(log_data))
        raise
    
def replay_message_sandi(body):
    status_mq = mqexchange.publish_sandi_message(body)
    body_j = json.loads(body)
    if status_mq:
        log_data = { "event": "Rabbitmq replay into sandi queue", "body": body_j }
        LOG.info(json.dumps(log_data))
    else:
        log_data = { "event": "Rabbitmq fail replay into sandi queue", "body": body_j }
        LOG.error(json.dumps(log_data))
        raise
    
@retry(wait=wait_fixed(2), stop=stop_after_attempt(3))
def fetch_with_retry(url):
    global headers, username, password
    
    response = requests.get(url, auth=HTTPBasicAuth(username, password))
    response.raise_for_status()  # Raise an error if the request fails
    return response

'''
notes:
If you would rather see the exception your code encountered at the end of the stack trace (where it is most visible), you can set reraise=True.
'''
@retry(wait=wait_fixed(2), stop=stop_after_attempt(3), reraise=True)
def post_gtsmessage(url, data):
    global headers, username, password
    
    response = requests.post(url, json=data, headers=headers, auth=HTTPBasicAuth(username, password))
    response.raise_for_status()  # Raise an error if the request fails
    return response

def is_six_digit_number(string):
    try:
        return bool(re.fullmatch(r"\d{6}", string))
    except:
        return False

def is_four_alpha_characters(string):
    try:
        return bool(re.fullmatch(r"[A-Za-z]{4}", string))
    except:
        return False
    
def is_valid_header(ttaaii, header_list):
    try:
        ttaa = ttaaii[:4]
        header = header_list.get(ttaa)

        if header is None:
            return False
        return True
    except:
        return False
    
def get_type_message(ttaaii, header_list):
    try:
        ttaa = ttaaii[:4]
        header = header_list.get(ttaa)

        if header is None or len(header["value"]) == 0:
            return None
        
        type_message = header["value"]
        if len(type_message) == 1:
            return f"0{type_message}"
        else:
            return type_message
    except:
        return None
