import csv
import serial

SERIAL_PORT = 'COM3'
SERIAL_BAUD = 57600
OUT_FILE = 'angle_encoders_gyro_getMotion_1.csv'
FS = 100
MEAS_DUR_SEC = 120

TS = 1.0 / FS
N_SAMPLES = int(MEAS_DUR_SEC * FS)

ser = serial.Serial(SERIAL_PORT, SERIAL_BAUD)
ser.flush()

with open(OUT_FILE, newline='', mode='w') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')

    for _ in range(N_SAMPLES):

        dataList= ser.readline().decode('utf-8').strip('\r\n').split(',')

        csvwriter.writerow(dataList)

ser.close()