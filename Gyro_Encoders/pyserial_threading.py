# Python required library
# pip install pyserial

import serial
import threading
import time


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
        info = [data[i:i + 2] for i in range(0, len(data), 2)]
        if len(info)!=0:
            x = int.from_bytes(info[0], "little", signed=True)
            y = int.from_bytes(info[1], "little", signed=True)
            theta = float(int.from_bytes(info[0], "little", signed=True))/10000 # we undo the scale implemented in Arduino, must be tha same
            print(x, y, theta)


my_Serial()

t1 = threading.Thread(target=my_Serial)
t1.daemon = True
t1.start()