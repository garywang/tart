import cv, time, sys
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
from tart.sensors import camera, vision, trig

if __name__=="__main__":
    try:
        #cam=camera.WebCam()
        vt=vision.VisionThread(debug=True)
        vt.start()
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        print "Ending Program"
    
    finally:
        vt.stop()

