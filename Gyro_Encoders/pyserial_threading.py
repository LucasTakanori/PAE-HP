# Python required library
# pip install pyserial

import serial
import threading
import time

global uart
uart = True

def my_Serial():
    global uart
    port = "/dev/ttyACM0" #defines the Arduino port COM3 on windows, /dev/ttyACM0 on linux
    ser = serial.Serial(port, baudrate=9600, timeout=0)
    count=0
    while uart:
        time.sleep(0.5)
        data = ser.read(6)
        ser.flushInput()
        #data_encoder = data.decode('utf8')
        data_encoder = int.from_bytes(data, "little", signed=False)
        #print(data_encoder)
        print(count , data)
        z = list(data)
        #x = int(list[1])+int(list[0])*255
        info = [data[i:i + 2] for i in range(0, len(data), 2)]
        if len(info)!=0:
            x = int.from_bytes(info[0], "little", signed=True)
            print(x)

        count = count + 1

my_Serial()

t1 = threading.Thread(target=my_Serial)
t1.daemon = True
t1.start()