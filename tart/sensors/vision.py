from PIL import Image, ImageFilter
from collections import deque
import math
import time
import threading
import cv


#Colors
RED=1           #ball
WHITE=2         #wall
BLUE=3          #top of wall
YELLOW=4        #center wall
PURPLE=5        #5-point line
GREEN=6         #bin
GRAY=0          #everything else

def get_color_from_hsv(hsv):
    h, s, v=hsv
    if s<0.35 and v>0.7:
        return WHITE
    elif s<0.4 or v<0.1:
        return GRAY
    elif h>340 or h<20:
        return RED
    elif h<260 and h>170:
        return BLUE
    else:
        return GRAY

def get_rgb_from_color(color):
    if color==RED:
        return (255, 0, 0)
    elif color==WHITE:
        return (255, 255, 255)
    elif color==BLUE:
        return (0, 0, 255)
    else:
        return (0, 0, 0)

def convert_to_colors(im):
    hsv=cv.CreateImage((im.width, im.height), cv.IPL_DEPTH_32F, 3)
    cv.ConvertScale(im, hsv, scale=1/255.)
    cv.CvtColor(hsv, hsv, cv.CV_BGR2HSV)
    colors=cv.CreateImage((im.width, im.height), cv.IPL_DEPTH_8U, 1)
    for i in range(im.height):
        for j in range(im.width):
            colors[i, j]=get_color_from_hsv(hsv[i, j])
    return colors
    
def convert_to_image(colors):
    rgb=cv.CreateImage((colors.width, colors.height), cv.IPL_DEPTH_32F, 3)
    for i in range(colors.height):
        for j in range(colors.width):
            rgb[i, j]=get_rgb_from_color(colors[i, j])
    cv.CvtColor(rgb, rgb, cv.CV_RGB2BGR)
    return rgb


def find_blobs(im, color=None, reverse=False):
    """Find connected components
    
    Returns a (lazy) sequence containing the connected components of 'arr'
    that have the given 'color'.  If 'color' is not given, all
    connected components with non-zero color are returned.  If 'reverse'
    is True, components are found starting from the bottom."""
    
    if not reverse:
        rows=range(im.height)
    else:
        rows=range(im.height-1, -1, -1)
    
    done=set()
    for i in rows:
        for j in range(im.width):
            
            if ( ((i, j) in done) or
                 (color is None and im[i, j]==0) or
                 (color is not None and im[i, j]!=color) ):
                continue
            
            #We've found a new component:
            done.add((i, j))
            current=list([(i, j)])
            que=deque([(i, j)])
            while(que):
                i, j=que.popleft()
                for ii, jj in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
                    if   (ii>=0 and ii<im.height and jj>=0 and jj<im.width and
                          (ii, jj) not in done and im[i, j]==im[ii, jj]):
                        done.add((ii, jj))
                        current.append((ii, jj))
                        que.append((ii, jj))
            yield current
    return



class VisionThread(threading.Thread):
    def __init__(self, cam):
        threading.Thread.__init__(self)
        self.cam=cam
        self.running=False
    
    def run(self):
        self.running=True
        while self.running:
            im=self.cam.get_image()
            small_im=cv.CreateImage((im.width/2, im.height/2), cv.IPL_DEPTH_8U, 3)
            cv.PyrDown(im, small_im);
            smaller_im=cv.CreateImage((im.width/4, im.height/4), cv.IPL_DEPTH_8U, 3)
            cv.PyrDown(small_im, smaller_im);
            
            colors=convert_to_colors(smaller_im)
            
            self.closest_ball=self.find_closest_ball(colors)
            print self.closest_ball
            self.colors=colors
            
            #time.sleep(0)
    
    def stop(self):
        self.running=False
    
    def find_closest_ball(self, im):
        for b in find_blobs(im, color=RED, reverse=True):
            if self.isBall(b):
                return b[0]         #TODO: convert to angles
        return None
    
    def isBall(self, blob):
        """Check if a list of pixels is a ball"""
        #TODO: check trig to see if size is reasonable
        return len(blob)>4




def show_image(im, name="foo", num=10):
    for i in range(num):
        cv.ShowImage(name, im)
        cv.WaitKey(10)
