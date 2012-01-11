import arduino

class Motor(arduino.Motor):
    """Motor wrapper class"""
    
    def setVal(self, val):
        """Takes a value from -127 (full reverse) to 127 (full forward)"""
        if(val<0):
            val=200-val
        arduino.Motor.setVal(self, val)
