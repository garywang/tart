import sys, time, math
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
import arduino
from tart.actuators import motor
from tart.sensors import camera
from tart.mapping import vision
from tart.mapping.trig import CameraInfo

if __name__=="__main__":
    try:
        ard = arduino.Arduino()
        motor0 = motor.Motor(ard,0)
        motor1 = motor.Motor(ard,1)
        vis=vision.VisionThread()

        ard.start()
        
        vis.start()
        time.sleep(1)
        
        while True:
            coords=vis.closest_ball
            if coords is None:
                motor0.setVal(50)
                motor1.setVal(50)
            else:
                x, y=coords
                angle=math.pi/2-atan2(y, x)     #Right is positive, left is negative
                if angle>math.pi/8:
                    motor0.setVal(-50)
                    motor1.setVal(-50)
                elif angle<-math.pi/8:
                    motor0.setVal(50)
                    motor1.setVal(50)
                else:
                    motor0.setVal(127)
                    motor1.setVal(-127)
            time.sleep(0.01)
        
    #This is so that when you hit ctrl-C in the terminal, all the arduino threads close. You can do something similar with threads in your program.
    except KeyboardInterrupt:
        print "Ending Program"
    
    finally:
        vis.stop()
        ard.stop()
