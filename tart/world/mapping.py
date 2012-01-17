import sys, pyximport; pyximport.install()
import math
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
from tart.world import vision2 as vision
from tart.world import odometry

class Map:
    
    def __init__(self):
        self.vis=vision.VisionThread(map=self)
        self.odometry=odometry.OdometryThread()
        self.closest_ball=None
    
    def start(self):
        self.vis.start()
        self.odometry.start()
    
    def stop(self):
        self.vis.stop()
        self.odometry.stop()
    
    def get_pos(self, vec=None, rel=None):
        """Get current position (x, y, theta)"""
        return self.odometry.get_pos()
    
    def get_abs_loc(self, vec, rel=None):
        """Get absolute location (x, y) of vec relative to current position or rel"""
        if rel is None:
            rel=self.odometry.get_pos()
        dx, dy=vec[0:2]
        x0, y0, theta=rel
        return (x0+dx*math.cos(theta)-dy*math.sin(theta), \
                y0+dx*math.sin(theta)+dy*math.cos(theta))
    
    def get_vector_to(self, loc, rel=None):
        """Get vector (dx, dy) to loc from current position or rel"""
        if rel is None:
            rel=self.odometry.get_pos()
        x0, y0, theta=rel
        x, y=loc[0:2]
        dx=x-x0
        dy=y-y0
        return (dx*math.cos(theta)+dy*math.sin(theta), \
               -dx*math.sin(theta)+dy*math.cos(theta))
    
    def get_speed(self):
        return self.odometry.get_speed()
    
    def update_balls(self, pos, balls):
        if len(balls)==0:
            self.closest_ball=None
        else:
            self.closest_ball=self.get_abs_loc(vec=balls[0], rel=pos)
    
    def get_closest_ball(self):
        """Return absolute location (x, y) of closest ball"""
        return self.closest_ball
