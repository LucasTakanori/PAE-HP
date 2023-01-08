import numpy as np
import matplotlib.pyplot as plt

DATA_FILE = 'angle_encoders_gyro_getMotion_-46_93_proba2.csv'

#Robot Constants ticksPerRev = 51200, wheelCirc = 768, wheelDist = 287;

dataArr = np.genfromtxt(DATA_FILE, delimiter=',')
#ts should be obtained from time, being the difference between the time of actual measurement - time of last measurement
#ts is always 122-123 ms

time = dataArr[:, 0]    #time in ms
wl = dataArr[:, 1]      #angular velocity of left wheel [deg/sec]
wr = dataArr[:, 2]      #angular velocity of right wheel [deg/sec]
wg = dataArr[:, 3]      #angular velocity of gyro [rad/sec] already scaled
ag = dataArr[:, 4]      #angle measured by integraation of angular velocity from gyro [degrees]

