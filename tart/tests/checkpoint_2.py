import sys, time
sys.path.append("/home/maslab-team-5/Maslab/tart/")
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
import arduino
from tart.actuators import motor

if __name__=="__main__":
    try:
        ard = arduino.Arduino()
        motor0 = motor.Motor(ard,0)
        motor1 = motor.Motor(ard,1)
        switch = arduino.AnalogSensor(ard,3)

        ard.start()
        while not ard.portOpened: time.sleep(0.001) #Wait for the arduino to be ready, before sending commands
        
        for i in range(300):
            value = switch.getValue()
            print "Sensor: " + str(value)
            if value > 0:
                print "Wall bumped"
                break
            motor0.setVal(127)
            motor1.setVal(-127)
        
        motor0.setVal(-127)
        motor1.setVal(127)
        time.sleep(1)

        ard.close()
    #This is so that when you hit ctrl-C in the terminal, all the arduino threads close. You can do something similar with threads in your program.
    except KeyboardInterrupt:
        print "Ending Program"
    
    finally:
        ard.killReceived=True
