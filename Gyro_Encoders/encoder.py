class Encoder():

    def __init__(self):
        # execute the base constructor
        self.x = 0
        self.y = 0
        self.yaw = 0
        self.state = True   #if state = true --> still

    def set_values(self,x,y,theta,state):
        self.x = x
        self.y = y
        self.yaw = theta
        self.state = state  
