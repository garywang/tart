import cv, time, sys
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
from tart.sensors import camera, vision

if __name__=="__main__":
    try:
        cam=camera.WebCam()
        vt=vision.VisionThread(cam)
        vt.start()
        time.sleep(1)
        while True:
            cv.ShowImage("asdf", vision.convert_to_image(vt.colors))
            cv.WaitKey(10)
            time.sleep(0.05)
    except KeyboardInterrupt:
        print "Ending Program"
    
    finally:
        vt.stop()

