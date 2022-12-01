from math import nan
import adafruit_mpu6050

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

class Gyro: 

    def __init__(self, i2c):
        mpu = adafruit_mpu6050.MPU6050(i2c)
        self.gyro = mpu.gyro
        self.angle = 0
        self.bias = 0

    def calibrate(self, still):
        bias=0
        mean = 0
        while still:                #provided by encoders
            bias = bias + self.gyro[2]
            mean += 1
        
        if mean > 0 : self.angle = bias/mean
        else : self.angle = nan     #is moving

        return self.angle

    def get_angle(self):
        return self.angle