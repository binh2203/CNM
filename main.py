import sys
from Adafruit_IO import MQTTClient
import random, time
from model_detect import detection
import base64

AIO_FEED_IDs = ['bong-den', 'khi-gas', 'nhan-dang', 'hinh-anh']
AIO_USERNAME = "diemcongbinh"
AIO_KEY = "aio_usHr97oZiLFz3STHCnDQnoCwfVJx"

def connected(client):
    print("Ket noi thanh cong ...")
    for AIO_FEED_ID in AIO_FEED_IDs:
        client.subscribe(AIO_FEED_ID)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)
    

def message(client , feed_id , payload):
    print("Nhan du lieu: " + payload + ", feed_id: " + feed_id)

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

cnt = 10
while True:
    cnt -= 1
    if cnt%5==0: # truyền hình ảnh sau 5 lần đếm (5s)
        image, result, conf = detection()
        client.publish('hinh-anh', image)
        client.publish('nhan-dang', result)
        #client.publish('test.do-chinh-xac', conf)
    if cnt == 0: # truyền thông tin nhiệt độ và độ ẩm sau 10 lần đếm (10s)
        #nhiet_do = random.randint(10, 40)
        khi_gas = random.randint(0, 600)
        #client.publish('nhiet-do', str(nhiet_do))
        client.publish('khi-gas', str(khi_gas))
        cnt = 10
    time.sleep(1)

