import sys
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
import arduino
from math import radians, sin, cos, sqrt

class SimpleDrive:
    """Simple drive class"""
    
    def __init__(self, ard, numL=0, numR=1):
        self.motorL = arduino.Motor(ard, 1, numL)
        self.motorR = arduino.Motor(ard, 1, numR)
    
    def drive(self, left, right):
        self.motorL.setValue(left)
        self.motorR.setValue(right)

class OmniDrive:
    """Omnidirectional drive with 3 omniwheels. Assumes positive motor outputs go clockwise and positive angle goes clockwise"""
    
    def __init__(self, ard, motorL=(1,0), motorR=(1,1), motorB=(2,0)):
        mcL, numL = motorL
        mcR, numR = motorR
        mcB, numB = motorB
        self.motorL = arduino.Motor(ard, mcL, numL) # front left
        self.motorR = arduino.Motor(ard, mcR, numR) # front right
        self.motorB = arduino.Motor(ard, mcB, numB) # back wheel. note: motor controller only does 2 motors. have to fix on arduino side.
    
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

if __name__ == "__main__":
    try:
        ard = arduino.ArduinoThread()
        dt = OmniDrive(ard)

        ard.start()
        success = ard.waitReady()
        
        dt.rotate(50)
        #dt.forward()
        #dt.translate(50, 90)
        time.sleep(5)
        
    finally:
        ard.stop()
