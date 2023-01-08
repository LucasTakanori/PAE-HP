import numpy as np
import matplotlib.pyplot as plt

DATA_FILE = 'zero_rate_gyro_calibrated_getMotion_BW_5.csv'
fs = 100

dataArr = np.genfromtxt(DATA_FILE, delimiter=',')
ts = 1.0 / fs

gx = dataArr[:, 0] 
gy = dataArr[:, 1] 
gz = dataArr[:, 2]


plt.figure()
plt.title('Calibrated gyro DLPF 5HZ')
plt.plot(gx, label='gx')
plt.plot(gy, label='gy')
plt.plot(gz, label='gz')
plt.ylabel('Rad/sec')
plt.grid(True, which="both", ls="-", color='0.65')
plt.legend()
plt.show()