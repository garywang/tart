import arduino

class Motor(arduino.Motor):
    """Motor wrapper class"""
    
    def setSpeed(self, speed):
        self.setValue(speed/127)
    
    #def setVal(self, val):
    #    """Takes a value from -127 (full reverse) to 127 (full forward)"""
    #    arduino.Motor.setVal(self, val)
