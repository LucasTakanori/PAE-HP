import time
import board
import adafruit_mpu6050

i2c = board.I2C()  # uses board.SCL and board.SDA
mpu = adafruit_mpu6050.MPU6050(i2c)

archi1=open("bias.txt","w")
bias = 0
mitja = 0
dt = 0.01

try:
    while True:
        bias = bias + mpu.gyro[2]
        mitja = mitja +1
        time.sleep(dt)
        if mitja == 500:
          print("Mostra")
          mitja = 0
          bias = bias / 500
          archi1.write("%f\n"%bias)
          bias = 0

except Exception:
    pass

archi1.close() 

