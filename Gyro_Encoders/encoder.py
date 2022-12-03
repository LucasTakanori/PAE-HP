
from contextlib import nullcontext
from math import nan
import time
import RPi.GPIO as GPIO

# Python required library
# pip install pyserial

import serial
from threading import Thread

class Encoder(Thread):

    def __init__(self):
        # execute the base constructor
        Thread.__init__(self)
        self.x = 0
        self.y = 0
        self.yaw = 0
        self.state = True   #if state = true --> still

    def set_values(self,x,y,theta,state):
        self.x = x
        self.y = y
        self.yaw = theta
        self.state = state  

    def run(self):
        port = "/dev/ttyACM0" #defines the Arduino port COM3 on windows, /dev/ttyACM0 on linux
        ser = serial.Serial(port, baudrate=9600, timeout=0)
        count=0
        while True:
            time.sleep(0.5)
            data = ser.read(6)
            ser.flushInput()
            info = [data[i:i + 2] for i in range(0, len(data), 2)]
            if len(info)!=0:
                x = int.from_bytes(info[0], "little", signed=True)
                y = int.from_bytes(info[1], "little", signed=True)
                theta = float(int.from_bytes(info[0], "little", signed=True))/10000 # we undo the scale implemented in Arduino, must be tha same
                state = True    # fins que no passem l'estat també
                print(x, y, theta, state)
                self.set_values(x,y,theta,state)



