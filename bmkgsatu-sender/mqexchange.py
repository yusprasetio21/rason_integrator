import json
from decouple import config
from dscommon.mqhandler import MqHandler
from datetime import datetime
from dscommon.log import LOG
  
mq = None

def init_mq():
    global mq
    mq = MqHandler(host=config('RABBITMQ_HOST'))

def publish_unk_message(message):
    status = mq.publish(config('RABBITMQ_UNKQ'), message)
    return status

def publish_sandi_message(message):
    status = mq.publish(config('RABBITMQ_MSGQ'), message)
    return status

'''
Consume sandi (message)
'''
def consume_message(callback):
    mq.start_consuming(config('RABBITMQ_MSGQ'), callback, auto_ack=False)
    
'''
Consume unknown sandi (message)
jika metadata stasiun invalid
'''
def consume_unk_message(callback):
    mq.start_consuming(config('RABBITMQ_UNKQ'), callback, auto_ack=False)

