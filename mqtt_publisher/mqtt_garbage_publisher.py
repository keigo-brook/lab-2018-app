import kafka
import json
import paho.mqtt.client as mqtt
import os

SUB_BROKER = os.environ['KAFKA_BROKER_1']
RESULT_TOPIC = 'garbage-result-smartphone'
MQTT_SERVER = os.environ['MQTT_SERVER']
MQTT_PORT = int(os.environ['MQTT_PORT'])
MQTT_PUB_TOPIC = 'garbage-detection-result'


def kafkaConsumer(topic):
    message = kafka.KafkaConsumer(topic, bootstrap_servers=[SUB_BROKER])
    return message


def on_mqtt_publish(client, data, mid):
    print("published")


if __name__ == '__main__':
    result_consumer = kafkaConsumer(RESULT_TOPIC)
    mqttc = mqtt.Client(client_id="LCESS", clean_session=False)
    mqttc.connect(MQTT_SERVER, MQTT_PORT, 60)
    mqttc.on_publish = on_mqtt_publish

    print("start listening from {}, {} to {}".format(SUB_BROKER, RESULT_TOPIC, MQTT_PUB_TOPIC))
    for message in result_consumer:
        print("message arrived: {}".format(message.value))
        mqttc.publish(MQTT_PUB_TOPIC, message.value, 0, True)
        
