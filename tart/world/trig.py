import math

def get_dist(vec1, vec2=(0,0,0)):
    x1, y1, z1=vec1
    x2, y2, z2=vec2
    d1, d2, d3=x1-x2, y1-y2, z1-z2
    return math.sqrt(d1*d1+d2*d2+d3*d3)

class CameraInfo():
    """Physical information about camera location, used as parameters for vision"""
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
        """Find the coordinates of an object relative to the camera
        
        Given:
            rc=(row, column), the lowest pixel of the object
            im, the image the pixel came from
            height, the height of the object above the ground"""
        r=(rc[0]+0.)/im.height
        c=(rc[1]+0.)/im.width
        dheight=self.cam_height-height
        y_angle=math.atan((1.-r)*math.sin(self.height_angle)/(r+(1.-r)*math.cos(self.height_angle)))
        y=dheight*math.tan(y_angle+self.low_angle)
        x=math.sqrt(y*y+dheight*dheight)*math.tan(self.width_angle/2)*2*(c-.5)
        return (x, y, -dheight)
    
    def get_pixel_size(self, rc, im):
        """Find the size of a pixel"""
        
        r, c=rc
        vec=self.get_vector(rc, im)
        vec1=self.get_vector((r, c+1), im)
        #vec2=self.get_vector((r-1, c), im)
        dist=get_dist(vec, vec1)
        
        return dist*dist
