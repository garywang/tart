import cv, time, sys
import pyximport; pyximport.install()
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
from tart.sensors import camera, vision, vision2, trig

if __name__=="__main__":
    try:
        #cam=camera.WebCam()
        vt=vision2.VisionThread(debug=True)
        vt.start()
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        print "Ending Program"
    
    finally:
        vt.stop()

