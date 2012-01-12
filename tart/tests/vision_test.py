import cv, time, sys
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
from tart.sensors import camera, vision, trig

if __name__=="__main__":
    try:
        #cam=camera.WebCam()
        info=trig.CameraInfo(cam_height=29., height_angle=0.70, width_angle=0.93, min_dist=28.)
        vt=vision.VisionThread(info, debug=True)
        vt.start()
        time.sleep(100)
    except KeyboardInterrupt:
        print "Ending Program"
    
    finally:
        vt.stop()

