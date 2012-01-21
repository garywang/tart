import sys, time
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
from tart.arduino import arduino
from math import radians, sin, cos, sqrt
from tart import params

class SimpleDrive:
    """Simple drive class"""
    
    def __init__(self, ard, motorL=(1,0), motorR=(1,1)):
        self.motorL = arduino.Motor(ard, motorL)
        self.motorR = arduino.Motor(ard, motorR)
    
    def setMotors(self, left, right):
        self.motorL.setValue(left)
        self.motorR.setValue(right)

    def rotate(self, value):
        self.setMotors(value, -value)

    def forward(self, rotation=0):
        if rotation >= 0:
            l = 127
            r = 127-rotation 
        elif rotation < 0:
            l = 127-rotation
            r = 127
        self.setMotors(l, r)

class OmniDrive:
    """Omnidirectional drive with 3 omniwheels.
    
    Assumes positive motor outputs go clockwise and positive angle goes clockwise"""
    
    def __init__(self, ard, motorL=params.omni_l, motorR=params.omni_r, motorB=params.omni_b):
        self.motorL = arduino.Motor(ard, motorL) # front left
        self.motorR = arduino.Motor(ard, motorR) # front right
        self.motorB = arduino.Motor(ard, motorB) # back
    
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
        ard = arduino.ArduinoThread(debug=True)
        dt = OmniDrive(ard)

        ard.start()
        success = ard.waitReady()
        
        dt.rotate(127)
        #dt.forward()
        #dt.translate(50, 90)
        time.sleep(100)
        
    finally:
        ard.stop()
