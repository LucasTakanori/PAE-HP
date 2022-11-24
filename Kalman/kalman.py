from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

class Kalman: 

 def __init__(self, fs, alpha0, omega0):
  self.fs = fs
  self.state = [alpha0, omega0]
  k = KalmanFilter (dim_x=2, dim_z=2)                       #initialization
  k.x = np.array([alpha0, omega0])                          #intial state (position and velocity)
  k.F = np.array([[1.,t],
                  [0.,1.]])                                 #define transition matrix
  k.H = np.array([[1.,t],
                  [0.,1.]])                                 #define measurement matrix
  k.P = np.array([[1000.,    0.],
                  [   0., 1000.] ])                         #define covariance matrix
  k.R = np.array([[0.05,    0.],
                  [   0., 0.05] ])                            #define measurement noise matrix
  k.Q = Q_discrete_white_noise(dim=2, dt=0.1, var=1)        #define process noise matrix
  self.k = k

  return k

 def angular_vector(alpha, omega, t):
    alpha = alpha + omega*t
    return [alpha, omega]

 def filtrar(self, measure, t):
   self.k.predict()
   self.k.update(self.angular_vector(self.k.x[0], measure, t))
   self.state = self.k.x
   return Kalman(self.fs, self.state, self.k )

def get_position(self):
    return self.state[0]

def get_velocity(self):
    return self.state[1]


def lectura(fichero):
    f = open(fichero, 'r')
    datos = []
    for linea in f:
     datos.append(float(linea.strip('\n')))
    return datos


# Lectura de fichero de prueba
fichero = 'datos3.txt'
datos = lectura(fichero)
fs = 100
t = 1/fs
longitud = len(datos)
tiempo = np.arange(0, (longitud)/100, t)
output = []

kal = Kalman(fs, 0, 0)

for i in range(longitud):
  kal.filtrar(datos[i], t)
  output.append(kal.x[1])

fig = plt.figure()
# plt.axis([0, 10, 0, 1])
plt.title('Data from gyroscope', fontweight='bold')
plt.xlabel('Time')
plt.ylabel('Velocity (rad/s)')
plt.plot(tiempo, datos, 'k',label='noisy measurements')
plt.plot(tiempo, output, 'r',label='Filter signal')
plt.show()

