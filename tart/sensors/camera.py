from PIL import Image, ImageFilter

__all__ = ['Camera', 'FileCamera']

class Camera(object):
    """An abstract class that represents sources of images"""
    
    def get_image(self):
        """Returns an Image object containing the current image"""
        return []

class FileCamera(Camera):
    """A Camera that reads images from files"""
    
    def __init__(self, file):
        self.file=file
    
    def get_image(self):
        im=Image.open(self.file)
        if im.mode != 'RGB':
            im=im.convert('RGB')
        im=im.filter(GaussianBlur(1))
        return im
        
        
class GaussianBlur(ImageFilter.Filter):
    name = "GaussianBlur"

    def __init__(self, radius=2):
        self.radius = radius
    def filter(self, image):
        return image.gaussian_blur(self.radius)