import sys, time
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
import arduino
from tart.actuators import drive
from tart.logic import state_machine
from tart.logic.states import State
from tart.sensors import sensor
from tart.world import mapping

class Shortcake:
    def __init__(self):
        self.ard = arduino.ArduinoThread()
        self.map = mapping.Map()
        self.sm = state_machine.StateMachine(self, ShortExploreState)
        self.drive = SimpleDrive(self.ard)

    def start(self):
        self.ard.start()
        self.map.start()
        self.ard.waitReady()

        self.start_time = time.time()
        self.sm.start()
        
    def stop(self):
        self.ard.stop()
        self.map.stop()
        self.sm.stop()
        
class ShortExploreState(State):
    def step(self):
        if self.map.get_visible_ball():
            return ShortRotateState(self.robot)
        
        self.drive.setMotors(-50, 50)
        return self

class ShortRotateState(State):
    def step(self):
        ball = self.map.get_visible_ball()
        if ball is None:
            return ShortExploreState(self.robot)
        vec = self.map.get_vector_to(ball)
        angle = self.map.get_angle(vec)
        if abs(angle) < 0.2:
            return ShortForwardState(self.robot)

        self.drive.rotate(angle/abs(angle)*127)
        return self

class ShortForwardState(State):
    def step(self):
        ball = self.map.get_visible_ball()
        if ball is None:
            return ShortExploreState(self.robot)
        vec = self.map.get_vector_to(ball)
        angle = self.map.get_angle(vec)
        if abs(angle) > 0.5:
            return ShortRotateState(self.robot)

        self.drive.forward()
        return self

class ShortEscapeState(State):
    def step(self):
        if time.time() - self.start_time > 1:
            return ShortExploreState(self.robot)
        self.drive.setMotors(127, -127)
        return self

if __name__=="__main__":
    try:
        bot = Shortcake()
        bot.start()

    #This is so that when you hit ctrl-C in the terminal, all the arduino threads close. You can do something similar with threads in your program.
    except KeyboardInterrupt:
        print "Ending Program"
    
    finally:
        bot.stop()
