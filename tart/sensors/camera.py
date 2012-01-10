import cv

__all__ = ['Camera', 'FileCamera']

class Camera(object):
    """A class that represents sources of images"""

class FileCamera(Camera):
    """A Camera that reads images from files"""
    
    def __init__(self, file):
        self.file=file
    
    def get_image(self):
        im=cv.LoadImage(self.file, iscolor=cv.CV_LOAD_IMAGE_COLOR)
        return im

