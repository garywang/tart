import sys, time
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries")
from tart.arduino import arduino

class HMotor:
    def __init__(self, ard, direction_port, brake_port, pwm_port):
        direction = arduino.DigitalOut(ard, direction_port)
        brake = arduino.DigitalOut(ard, brake_port)
        pwm = arduino.PWM(ard, pwm_port)

    def setValue(self, value): # between -127 and 127
        if value >= 0:
            direction.setValue(1)
        else:
            direction.setValue(0)
        brake.setValue(0)
        pwm.setValue(abs(value/127.))

    def brake(self, value=1): # between 0 (coast) and 1 (brake)
        brake.setValue(1)
        pwm.setValue(value)
