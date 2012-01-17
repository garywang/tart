import sys, time
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
import arduino
from tart.logic import state_machine
from tart.world import vision
from tart.control import pidrive
from tart.actuators import drive

class Cheesecake:
    def __init__(self):
        self.ard = arduino.ArduinoThread()
        self.vis = vision.VisionThread(self)
        #self.map = mapping.MappingThread(self) # not implemented. notes: arguments
        self.sm = state_machine.StateMachine(self)
	self.ctl = control.PIDriveThread(self)
	#self.cam = camera
	#self.bump = bump
        #self.dt = drive.OmniDrive(self.ard)
    
    def start(self):
        ard.start()
        vis.start()
        sm.start()
    
    def stop(self):
        ard.stop()
        vis.stop()
        sm.stop()

if __name__ == "__main__":
    try:
        bot = Robot()
        bot.start()
    
    except KeyboardInterrupt:
        print "Ending Program"
    
    finally:
        bot.stop()
