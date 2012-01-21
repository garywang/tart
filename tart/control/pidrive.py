import sys, time, math
import threading, thread
from tart.actuators import drive
from tart import params

class PIDriveController(drive.OmniDrive):
    def __init__(self, ard, map, debug=params.drive_debug):
        drive.OmniDrive.__init__(self, ard)
        self.map=map
        self.debug=debug
        self.drive_controller=PController(params.drive_drive_kp)
        self.rotate_controller=PController(params.drive_rotate_kp)
    
    def drive_to_point(self, point):
        """Use closed loop control to drive to a point"""
        if self.debug:
            print "drive to: "+str(point)
        
        v=self.map.get_vector_to(point)
        theta=self.map.get_angle(v)
        self.forward(self.drive_controller.step(theta))
    
    def rotate_toward_point(self, point):
        """Use closed loop control to rotate in place in direction of point"""
        if self.debug:
            print "rotate toward: "+str(point)
        
        v=self.map.get_vector_to(point)
        theta=self.map.get_angle(v)
        self.rotate(self.rotate_controller.step(theta))

class PController:
    def __init__(self, Kp, debug=False):
        self.Kp=Kp
        self.debug=debug
    
    def step(self, err):
        if self.debug:
            print err
        return self.Kp*err

class PIDController:
    def __init__(self, Kp, Ki, Kd, debug=False):
        self.Kp=Kp
        self.Ki=Ki
        self.Kd=Kd
        self.debug=debug
        self.last_err=None
        self.err_sum=0
    
    def step(self, err):
        if self.debug:
            print err, (err-self.last_err)/(time.time()-self.last_time), self.err_sum+err
        res=self.Kp*err
        if self.last_err is not None:
            res+=self.Kd*(err-self.last_err)/(time.time()-self.last_time)
        self.last_err=err
        self.last_time=time.time()
        self.err_sum+=err
        res+=self.Ki*self.err_sum
        return res
