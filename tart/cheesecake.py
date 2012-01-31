import sys, time
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
from tart.arduino import arduino
from tart.logic import state_machine
from tart.world import mapping
from tart.control import pidrive
from tart.sensors import sensor
from tart.actuators import motor

class Cheesecake:
    def __init__(self):
        self.ard = arduino.ArduinoThread()
        self.map = mapping.Map()
        self.sm = state_machine.StateMachine(self)
        self.drive = pidrive.PIDriveController(self.ard, self.map)
        self.roller = motor.get_motor(self.ard, (1, 0))
    
    def start(self):
        self.ard.start()
        self.map.start()
        assert self.ard.waitReady()
        button=sensor.BumpSensor(self.ard, 8)
        while not button.pressed():
            time.sleep(0.01)
        self.start_time = time.time()
        self.roller.setValue(127)
        self.sm.start()
    
    def stop(self):
        self.sm.stop()
        self.map.stop()
        self.drive.stop()
        self.ard.stop()

    def get_time(self):
        return time.time() - self.start_time

if __name__ == "__main__":
    try:
        bot = Cheesecake()
        bot.start()
        time.sleep(3*60+5)
    
    except KeyboardInterrupt:
        print "Ending Program"
    
    finally:
        try:
            bot.stop()
        except:
            pass
