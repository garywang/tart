import cv
import threading

class FileCamera():
    """A "camera" that reads images from files"""
    
    def __init__(self, file):
        self.file=file
    
    def get_image(self):
        im=cv.LoadImage(self.file, iscolor=cv.CV_LOAD_IMAGE_COLOR)
        return im

class RealCamera():
    """An actual camera"""
    
    def __init__(self, num):
        self.capture=cv.CaptureFromCAM(num)
    
    def get_image(self):
        return cv.QueryFrame(self.capture)

class WrapperCamera(threading.Thread):
    """Continuously call get_image of wrapped camera, return latest result"""
    
    def __init__(self, cam):
        threading.Thread.__init__(self)
        self.cam=cam
        self.lock=threading.Lock()
        self.start()
    
    def run(self):
        self.running=True
        while self.running:
            #self.lock.acquire()
            self.image=self.cam.get_image()
            #self.lock.release()
    
    def get_image(self):
        #self.lock.acquire()
        im=cv.CreateImage((self.image.width, self.image.height), cv.IPL_DEPTH_8U, 3)
        cv.Copy(self.image, im)
        #self.lock.release()
        return im
    
    def stop(self):
        self.running=False
