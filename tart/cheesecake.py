import sys, time
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
import arduino
from tart.logic import state_machine
from tart.world import mapping
#from tart.control import piddrive
from tart.actuators import drive

class Cheesecake:
    def __init__(self):
        self.ard = arduino.ArduinoThread()
        self.map = mapping.MappingThread()
        self.sm = state_machine.StateMachine(self)
        self.drive=drive.OmniDrive(self.ard)
	#self.ctl = piddrive.PIDDriveThread(self)
	#self.cam = camera
	#self.bump = bump
        #self.dt = drive.OmniDrive(self.ard)
    
    def start(self):
        ard.start()
        map.start()
        sm.start()
    
    def stop(self):
        ard.stop()
        map.stop()
        sm.stop()

if __name__ == "__main__":
    try:
        bot = Cheesecake()
        bot.start()
        time.sleep(3*60+5)
    
    except KeyboardInterrupt:
        print "Ending Program"
    
    finally:
        bot.stop()
