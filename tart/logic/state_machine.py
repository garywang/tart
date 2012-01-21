import sys, time
import threading, thread
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
import math
from tart.logic import states
from tart import params

class StateMachine(threading.Thread):
    def __init__(self, robot, debug=params.state_debug):
        threading.Thread.__init__(self)
        states.robot = robot
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

