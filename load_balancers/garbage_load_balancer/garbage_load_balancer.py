import base64
import json
import threading
import kafka
import socket
import os
import time
import Queue
import sys

SUB_BROKER = os.environ['KAFKA_BROKER_2']
PUB_BROKER = os.environ['KAFKA_BROKER_1']
STATUS_TOPIC="garbage-load-status"
IMG_TOPIC='capImgLab'
RESULT_TOPIC = 'garbage-result'
DEFAULT_RESULT_TOPIC = RESULT_TOPIC + '-default'
TASK_SERVER_NAME = 'garbage-detect-listener'
TASK_SERVER_PORT = 8194

producer = {}


def kafkaConsumer(topic):

    message = kafka.KafkaConsumer(topic, bootstrap_servers=[SUB_BROKER])

    return message


def produce(topic, message):
    if topic == '':
        topic = DEFAULT_RESULT_TOPIC
    if not topic in producer:
        producer[topic] = kafka.KafkaProducer(bootstrap_servers=PUB_BROKER)
    producer[topic].send(topic, message.encode())


def task(message):
    print("start task at {}".format(time.time()))
    time_log = {}
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((TASK_SERVER_NAME, TASK_SERVER_PORT))

    messrx = message.value
    strrx = messrx.decode()
    dictrx = json.loads(strrx)
    dictrx['img'] = base64.b64decode(dictrx['img'].encode())
    fname = dictrx['ts'] + "." + dictrx['type']

    # send YOLO
    data = dictrx['img']
    datalen = str(len(data))
    sock.send(datalen.encode())
    while True:
        rec_data = sock.recv(1024)
        rec_data = rec_data.decode()
        if rec_data == 'OK':
            break

    sock.send(data)
    time_log['send_to_detecter_finish'] = time.time()
    time_log['captured_at'] = dictrx['captured_at']
    if 'hostname' in dictrx.keys():
        time_log['from_hostname'] = dictrx['hostname']
    else:
        time_log['from_hostname'] = 'unknown'

    if 'filename' in dictrx.keys():
        image_file_name = dictrx['filename']
    else:
        image_file_name = 'no name'

    # print("send: {}".format(len(data)))

    # receive YOLO result
    result = "{{ \"filename\": {}, \"result\": ".format(image_file_name)
    rec_data_len = 0
    while True:
        data = sock.recv(4096)
        data = data.decode()
        if not data:
            break
	elif data.find('\n') >= 0:
            rec_data_len = int(data.split('\n')[0])
            result += data[data.find('\n')+1:]
            if len(data[data.find('\n')+1:]) >= rec_data_len:
                break
        else:
            result += data

    result += "}"

    time_log['receive_from_detecter_done'] = time.time()
    if 'publish_to' in dictrx.keys():
        produce(RESULT_TOPIC + dictrx['publish_to'], result)
        produce('', result)
    else:
        produce('', result)
    produce(STATUS_TOPIC, json.dumps(time_log))


q = Queue.Queue()
def worker():
    while True:
        item = q.get()
        task(item)
        q.task_done()


if __name__ == '__main__':
    img_consumer = kafkaConsumer(IMG_TOPIC)

    produce(STATUS_TOPIC, "start garbage load balancer at {}".format(time.time()))

    if len(sys.argv) < 2:
        print("./garbage_load_balancer.py num_of_workers")
        exit()

    num_worker_threads = int(sys.argv[1])
    print("start, num_of_workers={}".format(num_worker_threads))
    for i in range(num_worker_threads):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()

    for message in img_consumer:
        q.put(message)
