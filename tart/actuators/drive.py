import sys
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
import arduino
from math import radians, sin, cos, sqrt

class SimpleDrive:
    """Simple drive class"""
    
    def __init__(self, ard, numL, numR):
        self.motorL = arduino.Motor(ard, numL)
        self.motorR = arduino.Motor(ard, numR)
    
    def drive(self, left, right):
        self.motorL.setValue(left)
        self.motorR.setValue(right)

class OmniDrive:
    """Omnidirectional drive with 3 omniwheels. Assumes positive motor outputs go clockwise and positive angle goes clockwise"""
    
    def __init__(self, ard, numL, numR, numB):
        self.motorL = arduino.Motor(ard, num1) # front left
        self.motorR = arduino.Motor(ard, num2) # front right
        self.motorB = arduino.Motor(ard, num3) # back wheel. note: motor controller only does 2 motors. have to fix on arduino side.
    
    def setMotors(self, left, right, back):
        self.motorL.setValue(left)
        self.motorR.setValue(right)
        self.motorB.setValue(back)
    
    def rotate(self, value):
        self.setMotors(value, value, value)
    
    def translate(self, value, angle): # angle=0 is forward. this is mostly for theoretical purposes; in practice, will probably use something else for control
        rad = radians(angle)
        l = int(value*(-0.5*sin(rad) + 0.866*cos(rad)))
        r = int(value*(-0.5*sin(rad) - 0.866*cos(rad)))
        b = int(value*-sin(rad))
        self.setMotors(l, r, b)
    
    def forward(self, rotation=0): # drives full forward, rotating by value. good for controlled forward driving (i.e. approaching balls)
        if rotation >= 0:
            l = +127
            r = -127 + 2*rotation
        elif rotation < 0:
            l = +127 + 2*rotation
            r = -127
        b = rotation
        self.setMotors(l, r, b)
