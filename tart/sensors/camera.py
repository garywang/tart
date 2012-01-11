import cv, threading, time
from tart.sensors.trig import CameraInfo


class Camera():
    
    def __init__(self):
        self.info=None
    
    def get_image(self):
        pass
    
    def update(self):
        pass
    
    def stop(self):
        pass

class FileCamera(Camera):
    """A "camera" that reads images from files"""
    
    def __init__(self, file):
        self.file=file
    
    def get_image(self):
        im=cv.LoadImage(self.file, iscolor=cv.CV_LOAD_IMAGE_COLOR)
        return im

class RealCamera(Camera):
    """An actual camera"""
    
    def __init__(self, num, info):
        self.capture=cv.CaptureFromCAM(num)
        self.info=info
    
    def get_image(self):
        return cv.QueryFrame(self.capture)
    
    def update(self):
        cv.GrabFrame(self.capture)

class WrapperCamera(threading.Thread, Camera):
    """Continuously call get_image of wrapped camera, return latest result"""
    
    def __init__(self, cam):
        threading.Thread.__init__(self)
        self.cam=cam
        self.info=cam.info
        self.lock=threading.Lock()
        self.start()
    
    def run(self):
        self.running=True
        while self.running:
            #self.lock.acquire()
            #self.image=self.cam.get_image()
            self.cam.update()
            time.sleep(0.1)
            #self.lock.release()
    
    def get_image(self):
        #self.lock.acquire()
        #self.image=self.cam.get_image()
        #im=cv.CreateImage((self.image.width, self.image.height), cv.IPL_DEPTH_8U, 3)
        #cv.Copy(self.image, im)
        #self.lock.release()
        return self.cam.get_image()
    
    def stop(self):
        self.running=False

class WebCam(Camera):
    """Our webcam"""
    
    def __init__(self, wrapped=True):
        self.info=CameraInfo(cam_height=84., height_angle=0.70, width_angle=0.93, min_dist=88.)
        rc=RealCamera(1, self.info)
        if(wrapped):
            self.cam=WrapperCamera(rc)
        else:
            self.cam=rc
    
    def get_image(self):
        return self.cam.get_image()
    
    def stop(self):
        self.cam.stop()
