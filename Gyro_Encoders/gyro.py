import math
import adafruit_mpu6050

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

class Gyro: 

    def __init__(self, i2c):
        mpu = adafruit_mpu6050.MPU6050(i2c)
        mpu.gyro_range = adafruit_mpdu6050.GyroRange.RANGE_250_DPS
        self.gyro = mpu.gyro
        self.angle = 0
        self.bias = 0        
        self.mean = 0
        self.scale = (180/math.pi)*1.31

    def calibrate(self, still,dt):
        if still:                #provided by encoders
            self.bias = self.bias + self.gyro[2]
            self.mean += 1
        else:
            self.bias = self.bias/self.mean
            self.mean = 0
            self.angle = self.angle + (self.gyro[2]-self.bias)*dt*self.scale

        return self.angle

    def get_angle(self):
        return self.angle