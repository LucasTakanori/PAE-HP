# Python required library
# pip install pyserial

import serial
import threading
import time


uart = True

def my_Serial():
    global uart
    port = "COM3" #defines the Arduino port COM3 on windows, /dev/ttyACM0 on linux
    ser = serial.Serial(port, baudrate=9600, timeout=0)
    count=0
    while uart:
        time.sleep(0.2)
        data = ser.read(9)
        info = [data[i:i + 2] for i in range(0, len(data), 2)]
        if len(data)==9:
            ser.flush()
            #x = int.from_bytes(info[0], "little", signed=True)
            #y = int.from_bytes(info[1], "little", signed=True)
            #theta = float(int.from_bytes(info[2], "little", signed=False))/100 # we undo the scale implemented in Arduino, must be tha same
            #state = bool(int.from_bytes(info[3], "little", signed=False))
            #theta = float(int.from_bytes(data[4:7], "little", signed=False))/1000 # we undo the scale implemented in Arduino, must be tha same
            #state = bool(int.from_bytes(data[8], "little", signed=False))
            print(bool(data[8]))


my_Serial()

t1 = threading.Thread(target=my_Serial)
t1.daemon = True
t1.start()