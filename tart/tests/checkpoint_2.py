import sys, time
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
import arduino
from tart.actuators import drive
from tart.sensors import sensor

if __name__=="__main__":
    try:
        ard = arduino.ArduinoThread()
        dt = drive.SimpleDrive(ard)
        switch = sensor.BumpSensor(ard, 23)

        ard.start()
        assert ard.waitReady()
        
        dt.setMotors(127, 127)

        t = time.time()
        while time.time() - t < 10:
            print switch.getValue()
            if switch.pressed():
                print "Wall bumped"
                break
            time.sleep(0.01)
        
        dt.setMotors(0, 0)
        time.sleep(0.5)

        dt.setMotors(-127, -127)
        time.sleep(2)
        
        dt.setMotors(0, 0)

    #This is so that when you hit ctrl-C in the terminal, all the arduino threads close. You can do something similar with threads in your program.
    except KeyboardInterrupt:
        print "Ending Program"
    
    finally:
        ard.stop()
