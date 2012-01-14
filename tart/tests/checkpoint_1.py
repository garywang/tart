import sys, time
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
import arduino
from tart.actuators import drive

if __name__=="__main__":
    try:
        ard = arduino.Arduino()
        dt = drive.SimpleDrive(ard, 0, 1)

        ard.start()
        while not ard.portOpened: time.sleep(0.001) #Wait for the arduino to be ready, before sending commands

        dt.drive(127, -127)
        time.sleep(1)

        dt.drive(0, 0)

        ard.close()
    #This is so that when you hit ctrl-C in the terminal, all the arduino threads close. You can do something similar with threads in your program.
    except KeyboardInterrupt:
        print "Ending Program"
        ard.killReceived=True
        
