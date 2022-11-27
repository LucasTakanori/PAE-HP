import numpy as np

# Distance_travelled = 2*PI*radious_wheel*(tick_difference/ticks_wheel)

def diffdrive(v_r, v_l, t, l):

    global pose
    x = pose[0]
    y = pose[1]
    theta = pose[2]

    if (v_l == v_r):
        theta_n = theta
        x_n = x + v_l * t * np.cos(theta)
        y_n = y + v_l * t * np.sin(theta)

    else:
        R = l/2.0 * ((v_l + v_r) / (v_r - v_l))
        ICC_x = x - R * np.sin(theta)
        ICC_y = y + R * np.cos(theta)

        w = (v_r - v_l) / l

        dtheta = w * t

        x_n = np.cos(dtheta)*(x-ICC_x) - np.sin(dtheta)*(y-ICC_y) + ICC_x
        y_n = np.sin(dtheta)*(x-ICC_x) + np.cos(dtheta)*(y-ICC_y) + ICC_y
        theta_n = theta + dtheta

    return (x_n, y_n, theta_n)