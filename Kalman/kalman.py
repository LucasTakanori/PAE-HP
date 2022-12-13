from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise
import numpy as np
import matplotlib.animation as animation

class Kalman: 

    def __init__(self, fs, alpha0, omega0):
        self.fs = fs
        self.t = 1/fs
        self.encoder = [.0 , .0]
        self.state = [alpha0, omega0]
        k = KalmanFilter (dim_x=2, dim_z=2)                       #initialization
        k.x = np.array([alpha0, omega0])                          #intial state (position and velocity)
        k.F = np.array([[1.,(1/fs)],
                        [0.,1.]])                                 #define transition matrix
        k.H = np.array([[1.,(1/fs)],
                        [0.,1.]])                                 #define measurement matrix
        k.P = np.array([[1000.,    0.],
                        [   0., 1000.] ])                         #define covariance matrix
        k.R = np.array([[0.05,    0.],
                        [   0., 0.05] ])                          #define measurement noise matrix
        k.Q = Q_discrete_white_noise(dim=2, dt=0.1, var=1)        #define process noise matrix
        self.k = k                                                #define the kalman filter object

    def angular_vector(alpha, omega, t):
        alpha = alpha + omega*t
        return [alpha, omega]

    def filter(self, measure):
        #update_encoder()
        f1 = (self.encoder[0] + self.encoder[1]*self.t)/self.k.x[0]
        f2 = self.encoder[1]/f.x[1]
        self.k.F = np.array([[f1,    0.],
                  [   0., f2] ])
        self.k.predict()
        self.k.update(self.angular_vector(self.k.x[0], measure, self.t))
        self.state = self.k.x
        return self.state[1]

    def update_encoder(self):
        # read files
        return 0

    def get_position(self):
        return self.state[0]

    def get_velocity(self):
        return self.state[1]

    def read_file(file):
        f = open(file, 'r')
        data = []
        for row in f:
            data.append(float(row.strip('\n')))
        return data
