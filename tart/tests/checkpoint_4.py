import sys, time, math
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
import arduino
from tart.actuators import drive
from tart.sensors import camera
from tart.world import mapping

if __name__=="__main__":
    try:
        ard = arduino.Arduino()
        dt = drive.SimpleDrive(ard)
        vis = mapping.Map()

        ard.start()
        vis.start()
        assert ard.waitReady()
        
        t = time.time()
        while time.time() - t > 20:
            coords = vis.get_visible_ball()
            if coords is None:
                dt.setMotors(50, 50)    
            else:
                angle = vis.get_angle(coords)     #Right is positive, left is negative
                if angle > 0.2:
                    dt.rotate(50*angle)
                elif angle < -0.2:
                    dt.rotate(-50*angle)
                else:
                    dt.forward()
            time.sleep(0.01)
        
    #This is so that when you hit ctrl-C in the terminal, all the arduino threads close. You can do something similar with threads in your program.
    except KeyboardInterrupt:
        print "Ending Program"
    
    finally:
        vis.stop()
        ard.stop()
