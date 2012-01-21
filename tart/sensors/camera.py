import cv, threading, time
from tart.sensors.trig import CameraInfo
from tart import params


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
        cv.QueryFrame(self.capture)
    
    def stop(self):
        del(self.capture)

class WrapperCamera(threading.Thread, Camera):
    """Continuously call get_image of wrapped camera, return latest result"""
    
    def __init__(self, cam):
        threading.Thread.__init__(self)
        self.cam=cam
        self.info=cam.info
        self.im=None
        self.time=0
        self.last_time=0
        self.start()
    
    def run(self):
        self.running=True
        while self.running:
            self.im=self.cam.get_image()
            self.time=time.time()
            time.sleep(0.001)
        self.cam.stop()
    
    def get_image(self):
        while self.im is None or self.time==self.last_time:
            time.sleep(0.003)
        self.last_time=self.time
        return self.im
    
    def stop(self):
        self.running=False

class WebCam(Camera):
    """Our webcam"""
    
    def __init__(self, wrapped=params.webcam_wrapped, info=params.webcam_info, num=params.webcam_num):
        self.info=info
        rc=RealCamera(num, self.info)
        if(wrapped):
            self.cam=WrapperCamera(rc)
        else:
            self.cam=rc
    
    def get_image(self):
        return self.cam.get_image()
    
    def stop(self):
        self.cam.stop()
