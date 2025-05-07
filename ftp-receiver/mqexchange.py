import json
from decouple import config
from dscommon.mqhandler import MqHandler
from datetime import datetime
from dscommon.log import LOG
  
mq = None

def init_mq():
    global mq
    mq = MqHandler(host=config('RABBITMQ_HOST'))

def publish_message(message):
    status = mq.publish(config('RABBITMQ_MSGQ'), message)
    return status
