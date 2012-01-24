import sys, time
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
import arduino
from tart.actuators import drive

if __name__=="__main__":
    try:
        ard = arduino.Arduino(debug=True)
        dt = drive.SimpleDrive(ard, (2,0), (2,1))

        ard.start()
        assert ard.waitReady()

        dt.setMotors(127, 127)
        time.sleep(10)
        dt.setMotors(-127,-127)
        time.sleep(10)

        dt.setMotors(0, 0)

    #This is so that when you hit ctrl-C in the terminal, all the arduino threads close. You can do something similar with threads in your program.
    except KeyboardInterrupt:
        print "Ending Program"
    
    finally:
        ard.stop()
