import sys, time
import threading, thread
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
import math
from tart.logic import states, stuck
from tart import params
from tart.sensors.sensor import BumpSensor

class StateMachine(threading.Thread):
    def __init__(self, robot, debug=params.state_debug):
        threading.Thread.__init__(self)
        states.robot = robot
        states.stuck_detect = stuck.StuckDetector(robot)
        states.stuck_detect.robot = robot
        self.debug=debug
        self.running = False
        
    def run(self):
        self.running = True
        self.state = states.ScanState()
        while self.running:
            self.state = self.state.step()
            if self.debug:
                print self.state
            time.sleep(0)
    
    def stop(self):
        self.running = False

