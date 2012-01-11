import arduino

class BumpSensor(arduino.DigitalSensor):
    """Limit switch wrapper class"""
    
    def pressed(self):
        """Returns True if pressed, False otherwise"""
        return self.getValue() == 1
