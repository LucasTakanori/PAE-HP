import serial
import time

s = serial.Serial('/dev/ttyACM0',9600)
time.sleep(5)

while True:

  response = s.readline() 
  print(response)

s.close()
