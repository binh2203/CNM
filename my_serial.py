import serial

ser = None  # Initialize ser to None

def InitSerial():
    global ser
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = "COM5"
    ser.timeout = 10
    try:
        ser.open()
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")

def readSerial(client):
    global ser
    try:
        data = ser.readline().decode("latin-1").strip()
        processData(client, data)
    except serial.SerialException as e:
        print(f"Error reading serial port: {e}")

def processData(client, data):
    data = data.replace("T:", "")
    data = data.replace("H:", "")
    data = data.replace("G:", "")
    # data = data.replace("L:", "")
    splitData = data.split(",")
    if len(splitData) == 3:
        temperature = splitData[0]
        humidity = splitData[1]
        gas = splitData[2]
        # led = splitData[3]
        print("Cập nhật nhiệt độ: ", temperature)
        client.publish("nhiet-do", temperature)
        print("Cập nhật độ ẩm: ", humidity)
        client.publish("do-am", humidity)
        print("Cập nhật khí gas: ", gas)
        client.publish("khi-gas", gas)
        # print("Cập nhật bóng đèn: ", led)
        # client.publish("bong-den", led)
