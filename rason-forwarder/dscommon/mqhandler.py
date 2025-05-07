# Import libraries
import json
import pika
from pika.exceptions import AMQPConnectionError, ChannelClosedByBroker
import time
import atexit 
from dscommon.log import LOG

'''
Publish shared connection and channel
Consume shared connection but not channel each thread
Publish and Consume use separate connection
'''

heartbeat_interval = 60

class MqHandler():
    def __init__(self, host):
        self.host = host
        self.connection = None
        self.channel = None

        self.publish_connect(host)
        self.consume_connect(host)

        atexit.register(self.close)
        
    def publish_connect(self, host):
        retries = 0
        while retries < 10:
            try:
                self.publish_connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, heartbeat=heartbeat_interval))
                self.publish_channel = self.publish_connection.channel()
                self.publish_channel.basic_qos(prefetch_count=1) # one worker max 1 task at a time
                
                log_data = { "event": "Rabbitmq publish connected" }
                LOG.info(json.dumps(log_data))
                return True
            except Exception as e:
                log_data = { "event": "Rabbitmq publish connect failed", "error": str(e) }
                LOG.error(json.dumps(log_data))
                retries += 1
                time.sleep(5)
        return False
            
    def consume_connect(self, host):
        retries = 0
        while retries < 10:
            try:
                self.consume_connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, heartbeat=heartbeat_interval))
                
                log_data = { "event": "Rabbitmq consume connected" }
                LOG.info(json.dumps(log_data))
                return True
            except Exception as e:
                log_data = { "event": "Rabbitmq consume connect failed", "error": str(e) }
                LOG.error(json.dumps(log_data))
                retries += 1
                time.sleep(5)
        return False
    
    def is_publish_connected(self):
        return self.publish_connection is not None and self.publish_connection.is_open

    def is_consume_connected(self):
        return self.consume_connection is not None and self.consume_connection.is_open
    
    def get_publish_connection(self, force=False):
        # print(self.publish_connection.is_open, self.publish_channel.is_open)
        if not self.is_publish_connected() or force:
            stat = self.publish_connect(self.host)
            if not stat:
                return None, None
        return self.publish_connection, self.publish_channel
    
    def get_consume_connection(self, force=False):
        # print(self.publish_connection.is_open, self.publish_channel.is_open)
        if not self.is_consume_connected() or force:
            stat = self.consume_connect(self.host)
            if not stat:
                return None, None
        return self.consume_connection

    def consume_create_channel(self):
        try:
            consume_channel = self.consume_connection.channel()
            consume_channel.basic_qos(prefetch_count=1) # one worker max 1 task at a time
            
            log_data = { "event": "Rabbitmq consume channel created" }
            LOG.info(json.dumps(log_data))
            
            return consume_channel
        except Exception as e:
            log_data = { "event": "Rabbitmq consume channel create failed", "error": str(e) }
            LOG.error(json.dumps(log_data))
            
            return None
    
    def consume(self, consume_channel, queue, callback, auto_ack=True):
        try:
            if self.is_consume_connected() and consume_channel:
                consume_channel.queue_declare(queue=queue, durable=True)

                # def callback(ch, method, properties, body):
                #     print(f" [x] Received {body}")

                consume_channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=auto_ack)
            else:
                log_data = { "event": "Rabbitmq consuming failed" }
                LOG.error(json.dumps(log_data))
        except Exception as e:
            log_data = { "event": "Rabbitmq consuming failed", "error": str(e) }
            LOG.error(json.dumps(log_data))
    
    def publish(self, queue, body, exchange=''):
        try:
            conn, channel = self.get_publish_connection()
            if channel is None:
                log_data = {"event": "Rabbitmq publish failed, channel None"}
                LOG.error(json.dumps(log_data))
                return False
            
            # Pika may late to get connection lost so need extra precaution
            retries = 0
            while retries < 3:
                try:
                    channel.queue_declare(queue=queue, durable=True)
                    channel.basic_publish(exchange=exchange, routing_key=queue, 
                                            body=body, 
                                            properties=pika.BasicProperties(
                                                delivery_mode=pika.DeliveryMode.Persistent
                                            ))
                    return True
                except AMQPConnectionError:
                    conn, channel = self.get_publish_connection(force=True)
                    retries += 1
            
            log_data = {"event": "Rabbitmq publish failed, retry exceeded", "body": body}
            LOG.error(json.dumps(log_data))
            return False
        except Exception as e:
            log_data = {"event": "Rabbitmq publish failed", "error": str(e)}
            LOG.error(json.dumps(log_data))
            return False
            
    # def start_consuming(self, consume_channel):
    #     try:
    #         if self.is_consume_connected() and consume_channel:
    #             log_data = { "event": "Rabbitmq Start consuming all queue" }
    #             LOG.info(json.dumps(log_data))
    #             consume_channel.start_consuming()
    #         else:
    #             log_data = { "event": "Rabbitmq Start consuming failed" }
    #             LOG.error(json.dumps(log_data))
    #     except Exception as e:
    #         log_data = { "event": "Rabbitmq Start consuming failed", "error": str(e) }
    #         LOG.error(json.dumps(log_data))
    
    def start_consuming(self, queue, callback, auto_ack=True):
        """Start consuming messages with automatic reconnect on failure."""
        force = False
        while True:
            try:
                # Create a connection and channel
                conn = self.get_consume_connection(force)
                channel = self.consume_create_channel()

                self.consume(channel, queue, callback, auto_ack)
                
                log_data = { "event": "Rabbitmq Start consuming all queue" }
                LOG.info(json.dumps(log_data))

                # Start consuming messages
                channel.start_consuming()

            except (AMQPConnectionError, ChannelClosedByBroker) as e:
                force = True
                log_data = { "event": "Rabbitmq consumer lost connection, retrying...", "error": str(e) }
                LOG.warning(json.dumps(log_data))
                time.sleep(5)  # Delay before attempting to reconnect

            except Exception as e:
                log_data = { "event": "Rabbitmq consumer stopped", "error": str(e) }
                LOG.error(json.dumps(log_data))
                break  # Exit loop on an unexpected error
            
    def close(self):
        log_data = { "event": "MQ closed" }
        if self.publish_connection:
            self.publish_connection.close()
        if self.consume_connection:
            self.consume_connection.close()
        LOG.info(json.dumps(log_data))


def serialize_callback_info(ch, method, properties):
    log_data = {
        # Convert channel to a string representation or exclude it if not needed
        "channel": str(ch),  
        # Extract serializable attributes from `method`
        "method": {
            "consumer_tag": method.consumer_tag,
            "delivery_tag": method.delivery_tag,
            "exchange": method.exchange,
            "routing_key": method.routing_key,
        },
        # Extract serializable attributes from `properties`
        "properties": {
            "content_type": properties.content_type,
            "content_encoding": properties.content_encoding,
            "headers": properties.headers,
            "delivery_mode": properties.delivery_mode,
            "priority": properties.priority,
            "correlation_id": properties.correlation_id,
            "reply_to": properties.reply_to,
            "expiration": properties.expiration,
            "message_id": properties.message_id,
            "timestamp": properties.timestamp,
            "type": properties.type,
            "user_id": properties.user_id,
            "app_id": properties.app_id,
            "cluster_id": properties.cluster_id
        }
    }
    return log_data

if __name__ == '__main__':
    qu = MqHandler(host='localhost')