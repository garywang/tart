import sys, time
import threading
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
import math

class StateMachine(threading.Thread):
    def __init__(self, robot):
        threading.Thread.__init__(self)
        self.robot = robot
        
    def run(self):
        self.state = self.scan
        while True:
            self.state = self.state()
            time.sleep(0)
    
    def scan(self):
        if self.robot.vis.get_closest_ball(): # sees a ball
            return self.approach
        self.robot.dt.drive(127, -127)
        return self.scan
    
    def approach(self):
        if self.robot.vis.get_closest_ball() is None:
            return self.scan
        x, y = self.robot.vis.get_closest_ball()
        # this stuff should go in control eventually.
        angle=math.pi/2-atan2(y, x)     #Right is positive, left is negative
        if angle>math.pi/8:
            self.robot.dt.drive(-50, -50)
        elif angle<-math.pi/8:
            self.robot.dt.drive(50, 50)
        else:
            self.robot.dt.drive(127, -127)
        return self.approach

if __name__ == '__main__':
    sm = StateMachine()
    sm.start()
