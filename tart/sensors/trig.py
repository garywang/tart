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
    
    def get_vector(self, rc, im, height=0):
        r=(rc[0]+0.)/im.height
        c=(rc[1]+0.)/im.width
        dheight=self.cam_height-height
        y_angle=math.atan((1.-r)*math.sin(self.height_angle)/(r+(1.-r)*math.cos(self.height_angle)))
        y=dheight*math.tan(y_angle+self.low_angle)
        x=math.sqrt(y*y+dheight*dheight)*math.tan(self.width_angle/2)*2*(c-.5)
        return (x, y, height)
