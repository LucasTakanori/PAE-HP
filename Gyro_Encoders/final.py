import matplotlib.pyplot as plt

import time
from datetime import datetime
import board
import gyro
import RPi.GPIO as GPIO
import encoder
import serial

import sys 
sys.path.append('./Kalman')
import kalman as kal

GPIO.setmode(GPIO.BCM)


i2c = board.I2C()   # uses board.SCL and board.SDA
gyro = gyro.Gyro(i2c)

e = encoder.Encoder()

fs = 90.909090
dt = 1/fs

gyro_angles = []
output_angles = []

kalman_gyro = kal.Kalman(fs,0,0)

def graph(fs,array_d,array_o):
    t=1/fs
    plt.title('Data from gyroscope', fontweight='bold')
    plt.xlabel('Time')
    plt.ylabel('Velocity (rad/s)')
    plt.plot(t, array_d, 'k',label='noisy measurements')
    plt.plot(t, array_o, 'r',label='Filter signal')
    plt.show()

if __name__ == "__main__"():
    try:
        port = "/dev/ttyACM0"   # defines the Arduino port COM3 on windows, /dev/ttyACM0 on linux
        ser = serial.Serial(port, baudrate=9600, timeout=0)
        while True:
            data = ser.readline()
            # info = [data[i:i + 2] for i in range(0, len(data), 2)]
            if len(data)==11:    # it receives data from the arduino
                x = int.from_bytes(data[0:1], "little", signed=True)
                y = int.from_bytes(data[2:3], "little", signed=True)
                theta = float(int.from_bytes(data[4:7], "little", signed=False))/1000   # we undo the scale implemented in Arduino, must be tha same
                state = bool(data[8])   # until the state is obtained, if it's not 0, it will be True
                print(x, y, theta, state)
                e.set_values(x,y,theta,state)      
                print("Value of encoders is {}".format(e.x,e.y))
                time.sleep(dt)

                angle = gyro.calibrate(e.state,dt)
                print(angle)    # >> 2&1 dades_gyro.txt

                if e.state :
                    print("Yaw angle in º/sec before kalman filter: %.2f"%gyro.get_angle())
                    gyro_angles.append(gyro.get_angle())
                    gyro_state = kalman_gyro.filter(angle)
                    output_angles.append(gyro_state)
                    print(f"Angle turned: {gyro_state}")
                elif len(gyro_angles)>0:
                    graph(fs,gyro_angles,output_angles)
                    # save angles when state is moving
                    f = open (str(datetime.now()),'w')
                    f.write(f"gyro angles: {gyro_angles}\nfiltered angles: {output_angles}")
                    f.close()
                    gyro_angles = []
                    output_angles = []

    except Exception:
        pass
    
    GPIO.cleanup()
