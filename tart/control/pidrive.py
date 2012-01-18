import sys, time, math
import threading, thread
from tart.actuators import drive

class PIDriveController(drive.OmniDrive):
    def __init__(self, ard, map):
        drive.OmniDrive.__init__(self, ard)
        self.map=map
    
    def drive_to_point(self, point):
        """Use closed loop control to drive to a point"""
        dx, dy=self.map.get_vector_to(point)
        theta=math.pi/2-math.atan2(dy, dx)
        self.forward(100*theta)

    def rotate_toward_point(self, point):
        """Use closed loop control to rotate in place in direction of point"""
        dx, dy=self.map.get_vector_to(point)
        theta=math.pi/2-math.atan2(dy, dx)
        self.rotate(100*theta)
