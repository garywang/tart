import sys, time
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries")
from tart.arduino import arduino

class HMotor:
    def __init__(self, ard, direction_port, brake_port, pwm_port):
        self.direction = arduino.DigitalOut(ard, direction_port)
        self.brake = arduino.DigitalOut(ard, brake_port)
        self.pwm = arduino.PWM(ard, pwm_port)

    def setValue(self, value): # between -127 and 127
        if value > 0:
            self.brake.setValue(0)
            self.direction.setValue(1)
        elif value < 0:
            self.brake.setValue(0)
            self.direction.setValue(0)
        else:
            self.brake.setValue(1)
        self.pwm.setValue(abs(value/127.))

    def coast(self):
        self.brake.setValue(0)
        self.pwm.setValue(0)

if __name__=="__main__":
    try:
        ard = arduino.ArduinoThread(debug=True)
        motor = HMotor(ard, 22, 23, 2)
        ard.start()
        assert ard.waitReady()

        motor.setValue(127)
        time.sleep(1)
        
    #This is so that when you hit ctrl-C in the terminal, all the arduino threads close. You can do something similar with threads in your program.
    except KeyboardInterrupt:
        print "Ending Program"
    
    finally:
        ard.stop()
