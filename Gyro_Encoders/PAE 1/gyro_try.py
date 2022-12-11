
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
dt = 0
angle = 0.0
scale = 180/math.pi*1.31
first_try = 1

print ("Wait for initialization")

if first_try:
    time.sleep(1)
    first_try = 0


first_time = time.time_ns #time is defined as ns
#aqui s'haura de  fer respecte els encoders (quan estigin quiets)
while time.time_ns - first_time < 100000000:
	bias = bias +  mpu.gyro[2]
	mitja = mitja + 1

bias = bias / mitja
print (bias)
dt = (time.time_ns - first_time)*10^-9
print (bias * dt)


try:
    while True:

        count = 0
        first_time = time.time_ns
        while time.time_ns - first_time < 100000000:
            gyro = mpu.gyro
            m = gyro[2] - bias
            #print("Z:%f\n"%m)
        # quan encoders quiets no sumem 
        dt = (time.time_ns - first_time)*10^-9
        angle = angle + scale*m*dt
        print (angle)
        archi1.write("%f\n"%angle)

except Exception:
    pass

archi1.close() 
