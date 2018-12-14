import kafka
import json
import base64
import cv2
import sys
import datetime
import time
import csv
import os

BROKER = os.environ('KAFKA_BROKER_1')
TOPIC="capImgLab2"

QUALITY=3
SLEEP=0.1

def connect(broker):

	kafka_client = kafka.KafkaClient(broker)
	producer = kafka.SimpleProducer(kafka_client)

	#producer = kafka.KafkaProducer(bootstrap_servers=broker)

	return producer

def readInput(input):

	#message = cv2.imread(input)
	message = open(input,'rb').read()

	return message

def capImg(cam):

	ret, frame = cam.read()

	encode_param = [int(cv2.IMWRITE_PNG_COMPRESSION), QUALITY]
	result, encImg = cv2.imencode('.png', frame, encode_param)

	return encImg

def produce(producer, topic, message):

	producer.send_messages(topic, message)
	#producer.send(topic, message)
	#producer.flush()

def getTime():

	time = datetime.datetime.now()
	charTime = time.strftime('%Y%m%d-%H_%M_%S')

	return charTime

def jsonData(nowTime, cam):

	img = capImg(cam)

	#fname = nowTime + ".png"
	#writeData(fname, img)

	size = sys.getsizeof(img)
	binImg = base64.b64encode(img).decode('utf-8')
	
	dictdata = {
                "hostname": "raspi@10.0.0.19",
		"type": "png",
		"ts": nowTime,
                "captured_at": str(time.time()),
                "publish_to": "cam2",
		"size": size,
		"img": binImg,
	}
	
	return dictdata

def calcTh(data, time):

	return data * 8 / time / 1000000

def writeData(fname, data):

	open(fname, 'wb').write(data)

def setLOG(fname):

	f = open(fname, 'a')
	writer = csv.writer(f, lineterminator='\n')

	return writer


if __name__ == '__main__':

	producer = connect(BROKER)
	cam = cv2.VideoCapture(0)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

	#logCSV = setLOG('logCapImg.csv')

	log = []
	flag=1

        consumer = connect(BROKER)
        now = time.time()

	while(flag==1):

		nowTime = getTime()
		dictdata = jsonData(nowTime, cam)

		message = json.dumps(dictdata)
		binmessage = message.encode()

		start = time.time()
		produce(producer, TOPIC, binmessage)
		elapsedTime = time.time() - start

		throughput = calcTh(sys.getsizeof(binmessage), elapsedTime)

		#fname = dictdata['ts'] + "." + dictdata['type']
		#writeData(fname, dictdata['img'])

		log = [nowTime, throughput]
		#print(log)		
		#logCSV.writerow(log)

                time.sleep(SLEEP)
                #if time.time() - now > 60:
                #    time.sleep(60)
                #    now = time.time()
                #else:
		#    time.sleep(SLEEP)

	cam.release()
	#f.close()
