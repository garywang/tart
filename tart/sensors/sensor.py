from tart.arduino import arduino

class BumpSensor(arduino.DigitalSensor):
    """Limit switch wrapper class"""
    
    def pressed(self):
        """Returns True if pressed, False otherwise"""
        return self.getValue() == 0

class ShortIR(arduino.AnalogSensor):
	"""Short IR wrapper class"""

	def get_dist(self):
		"""Returns a distance in inches"""
        val = self.getValue()
		raise NotImplementedError
