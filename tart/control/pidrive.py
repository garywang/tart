import sys, time
import threading, thread
from tart.actuators import drive

class PIDriveController(drive.OmniDrive):
    def __init__(self, ard, map):
        drive.OmniDrive.__init__(self, ard)
    
    def drive_to_point(self, point):
        """Use closed loop control to drive to a point"""
        pass

    def rotate_toward_point(self, point):
        """Use closed loop control to rotate in place in direction of point"""
        pass
