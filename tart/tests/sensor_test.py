import sys, time
sys.path.append("/home/maslab-team-5/Maslab/tart/")
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
import arduino
from tart.actuators import motor
from tart.sensors import sensor

if __name__=="__main__":
    try:
        ard = arduino.Arduino()
        IRSensor = arduino.AnalogSensor(ard,0)

        ard.start()
        while not ard.portOpened: time.sleep(0.001) #Wait for the arduino to be ready, before sending commands
        
        for i in range(300):
            print "Sensor: " + str(IRSensor.getValue())

        ard.close()
    #This is so that when you hit ctrl-C in the terminal, all the arduino threads close. You can do something similar with threads in your program.
    except KeyboardInterrupt:
        print "Ending Program"
    
    finally:
        ard.killReceived=True
