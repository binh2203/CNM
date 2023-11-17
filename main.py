import sys
from Adafruit_IO import MQTTClient
import time
from ai import *
from my_serial import *
AIO_USERNAME = "diemcongbinh"
AIO_KEY = "aio_WYOi77YbffVRne2KKQTFTNxwaOBD"

feeds = ["bong-den", "nhiet-do", "do-am", "khi-gas", "ai"]

def connected(client): 
    print("Ket noi thanh cong ...") 
    for i in feeds:
        client.subscribe(i)

def subscribe(client , userdata , mid , granted_qos): 
    print("Subscribe thanh cong ...")

def disconnected(client): 
    print("Ngat ket noi ...") 
    sys.exit (1)

def message(client , feed_id , payload): 
    print("Nhan du lieu "+ feed_id +" : " + payload)

client = MQTTClient(AIO_USERNAME , AIO_KEY) 
client.on_connect = connected 
client.on_disconnect = disconnected 
client.on_message = message 
client.on_subscribe = subscribe 
client.connect() 
client.loop_background() 
counter = 2
sensor_type = 0
counter_ai = 5
InitSerial()
while True:
    counter = counter - 1
    if counter <= 0:
        readSerial(client)
        counter = 2
    # counter_ai = counter_ai -1
    # if counter_ai <= 0:
    #     counter_ai = 5
    #     ai_result = image_detector()
    #     print("AI output", ai_result)
    #     client.publish(feeds[4], ai_result)
    time.sleep(1)
 



 



