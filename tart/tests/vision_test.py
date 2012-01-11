import cv, time, sys
sys.path.append("/home/maslab-team-5/Maslab/tart/")
from tart.sensors import camera, vision

if __name__=="__main__":
    try:
        rc=camera.RealCamera(1)
        wc=camera.WrapperCamera(rc)
        vt=vision.VisionThread(wc)
        #vt=vision.VisionThread(rc)
        vt.start()
        time.sleep(1)
        while True:
            cv.ShowImage("asdf", vision.convert_to_image(vt.colors))
            cv.WaitKey(10)
    except KeyboardInterrupt:
        print "Ending Program"
    
    finally:
        vt.stop()
        wc.stop()
