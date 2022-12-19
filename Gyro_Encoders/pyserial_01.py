# Python required library
# pip install pyserial

import serial
import time


def my_Serial():

    port = "COM3" #defines the Arduino port COM3 on windows, /dev/ttyACM0 on linux
    ser = serial.Serial(port, baudrate=9600)

    while True:

        print("---------")
        #print(ser.is_open)
        #print("Please enter some input:")
        #user_input = input()
        data=ser.readline()
        print(data)
        print(len(data))
        x = int.from_bytes(data[0:1], "little", signed=True)
        y = int.from_bytes(data[2:3], "little", signed=True)
        theta = float(int.from_bytes(data[4:7], "little", signed=False))/1000   # we undo the scale implemented in Arduino, must be tha same
        state = bool(data[8])   # until the state is obtained, if it's not 0, it will be True
        print(x, y, theta, state)
        ser.reset_input_buffer()
    if False:
        print("Please enter some input:")
        user_input = input()
        
        ser.write(b"1")
        while ser.in_waiting < 9:
            count=0
        data = ser.read(9)
        #info = [data[i:i + 2] for i in range(0, len(data), 2)]
        if len(data)==9:
            x = int.from_bytes(data[0:1], "little", signed=True)
            y = int.from_bytes(data[2:3], "little", signed=True)
            #theta = float(int.from_bytes(info[2], "little", signed=False))/100 # we undo the scale implemented in Arduino, must be tha same
            #state = bool(int.from_bytes(info[3], "little", signed=False))
            theta = float(int.from_bytes(data[4:7], "little", signed=False))/1000 # we undo the scale implemented in Arduino, must be tha same
            state = bool(data[8])
            print(x,y,theta, state)
            #ser.reset_input_buffer()
            #ser.reset_output_buffer()
            #uart = False


my_Serial()

#t1 = threading.Thread(target=my_Serial)
#t1.daemon = True
#t1.start()
#t1.join()