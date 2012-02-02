import sys, time
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
from tart.arduino import arduino

class BumpSensor(arduino.DigitalSensor):
    """Limit switch wrapper class"""
    
    def pressed(self):
        """Returns True if pressed, False otherwise"""
        return self.getValue() == 0

class ShortIR(arduino.AnalogSensor):
    """Short IR (Sharp 2Y0A21) wrapper class"""

    def get_dist(self):
        """Returns a distance in cm"""
        val = self.getValue()
        if val < 0.4:
            return 100
        elif val > 2.5:
            return 0
        else:
            return 24./(val-0.1)

if __name__ == "__main__":
    try:
        ard = arduino.Arduino()
        bump = BumpSensor(ard, 8)
        ir = ShortIR(ard, 8)

        ard.start()
        ard.waitReady()
        
        for i in range(100):
            print ir.get_dist()
            time.sleep(0.1)
    finally:
        ard.stop()
