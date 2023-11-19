import sys
from Adafruit_IO import MQTTClient
import time
from model_detect import *
from my_serial import *
AIO_USERNAME = "diemcongbinh"
AIO_KEY = "aio_ItNh24gR0TeLGyhFiWaUvFzu1QVi"

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
    if feed_id == feeds[0]:
        if payload == "0":
            writeSerial("L0")
            print("Tắt bóng đèn!")
        elif payload == "1":
            writeSerial("L1")
            print("Bật bóng đèn!")


client = MQTTClient(AIO_USERNAME , AIO_KEY) 
client.on_connect = connected 
client.on_disconnect = disconnected 
client.on_message = message 
client.on_subscribe = subscribe 
client.connect() 
client.loop_background() 
sensor_type = 0
InitSerial()
cnt = 10
while True:
    cnt -= 1
    if cnt%5==0: # truyền hình ảnh sau 5 lần đếm (5s)
        image, result, conf = detection()
        client.publish('hinh-anh', image)
        client.publish('nhan-dang', result)
        print("Nhận dạng: " + str(result))
        print("Độ chính xác: " + str(conf))
    if cnt == 0: # truyền thông tin nhiệt độ và độ ẩm sau 10 lần đếm (10s)
        readSerial(client)
        cnt = 8
    time.sleep(1)
    




 



