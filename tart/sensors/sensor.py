import arduino

class BumpSensor(arduino.AnalogSensor):
    """Limit switch wrapper class"""
    
    def pressed(self):
        """Returns True if pressed, False otherwise"""
        return self.getValue > 0
