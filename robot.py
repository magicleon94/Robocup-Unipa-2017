class robot:
    def __init__(self,x,y,theta):
        self.x = x
        self.y = y
        self.theta = theta

    def updatePosition(self,newX,newY,newTheta):
        self.x = newX
        self.y = newY
        self.theta = newTheta

    
