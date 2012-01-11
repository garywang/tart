import math

class CameraInfo():
    
    def __init__(self, cam_height, height_angle, width_angle, min_dist):
        
        #height of camera from the ground
        self.cam_height=cam_height+0.
        
        #field of view of camera
        self.height_angle=height_angle+0.
        self.width_angle=width_angle+0.
        
        #shortest distance that the camera can see on the ground
        self.min_dist=min_dist+0.
        self.low_angle=math.atan(self.min_dist/self.cam_height)
    
    def get_vector(rc):
        row=rc[0]+0.
        col=rc[1]+0.
        y=math.tan(math.atan((1.-r)*math.sin(self.height_angle)/(r+(1.-r)*math.cos(self.height_angle))) \
                    +self.low_angle)
        return y