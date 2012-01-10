import sys
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
import arduino

class Motor(arduino.Motor):
    """Motor wrapper class"""
    
    def setVal(self, val):
        '''Takes a value from -127 to 127'''
        if(val<0):
            val=200-val
        arduino.Motor.setVal(self, val)
