
# -*- coding: utf-8 -*-
import time
import board
import adafruit_mpu6050
import math

i2c = board.I2C()  # uses board.SCL and board.SDA
mpu = adafruit_mpu6050.MPU6050(i2c)
mpu.gyro_range = adafruit_mpu6050.GyroRange.RANGE_250_DPS

archi1=open("90.txt","w")
bias = 0
mitja = 0
dt = 0.01
angle = 0.0
scale = 180/math.pi*1.31

print ("STOP 30 seconds")

#aqui s'haura de  fer respecte els encoders (quan estigin quiets)
while mitja < 300:
        bias = bias +  mpu.gyro[2]
        mitja = mitja + 1
        time.sleep(dt)

bias = bias / 300
print (bias)
print (bias * dt)


try:
    while True:
        gyro = mpu.gyro
        m = gyro[2] - bias
        print("Z:%f\n"%m)
        # quan encoders quiets no sumem 
        angle = angle + scale*m*dt
        print (angle)
        print(time.perf_counter())
        archi1.write("%f\n"%angle)

except Exception:
    pass

archi1.close() 

