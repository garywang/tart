import sys
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
import arduino

class SimpleDrive:
    """Simple drive class"""
    
    def __init__(self, ard, numL, numR):
        self.motorL = arduino.Motor(ard, numL)
        self.motorR = arduino.Motor(ard, numR)
    
    def drive(self, left, right):
        self.motorL.setValue(left)
        self.motorR.setValue(right)
