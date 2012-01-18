import sys, time
import threading, thread
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
import math
from tart.logic import states

class StateMachine(threading.Thread):
    def __init__(self, robot):
        threading.Thread.__init__(self)
        states.robot = robot
        self.running = False
        
    def run(self):
        self.running = True
        
        self.state = states.ScanState()
        while self.running:
            self.state = self.state.step()
            time.sleep(0)
    
    def stop(self):
        self.running = False

