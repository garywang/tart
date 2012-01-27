import sys
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries")
from tart.arduino import arduino
from tart.actuators import hbridge

def get_motor(ard, ports):
    if len(ports)==2:
        return arduino.Motor(ard, ports)
    elif len(ports)==3:
        return hbridge.HMotor(ard, ports[0], ports[1], ports[2])
