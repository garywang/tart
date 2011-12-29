from PIL import Image, ImageFilter
from collections import deque
import math
import time
import threading



def image_to_arr(im, func=None):
    """Convert Image to 2d list
    
    Given an Image object, returns a 2d list containing all the pixels in the
    Image.  If func is given, func is applied to each pixel."""
    data=im.load()
    arr=[];
    for i in range(im.size[1]):
        arr.append([])
        for j in range(im.size[0]):
            if func is None:
                arr[i].append(data[j, i])
            else:
                arr[i].append(func(data[j, i]))
    return arr

def arr_to_image(arr, func=None, mode='RGB'):
    """Convert 2d list to Image
    
    Given a 2d list, returns an Image object where each pixel is an item in
    the list.  If func is given, func is applied to each item."""
    image=Image.new(mode, (len(arr[0]), len(arr)))
    data=image.load()
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if func is None:
                data[j, i]=tuple(arr[i][j])
            else:
                data[j, i]=func(arr[i][j])
    return image




def rgb_to_hsv(rgb):    #rgb, not rgt
    """Given a tuple of values in rgb, return a tuple of values in hsv"""
    
    r, g, b=rgb[0]/255., rgb[1]/255., rgb[2]/255.
    
    v=max(r, g, b)
    delta=v-min(r, g, b)
    
    if v==0:
        return (0, 0, 0)
    
    s=delta/v
    
    if delta==0:
        h=0
    elif r==v:
        h=(g-b)/delta
    elif g==v:
        h=2+(b-r)/delta
    else:
        h=4+(r-g)/delta
    
    if h<0:
        h+=6
    
    return (h*60, s, v)
    

#Colors
RED=1           #ball
WHITE=2         #wall
BLUE=3          #top of wall
YELLOW=4        #center wall
PURPLE=5        #5-point line
GREEN=6         #bin
GRAY=0          #everything else

def hsv_to_color(hsv):
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

def color_to_rgb(color):
    if color==RED:
        return (255, 0, 0)
    elif color==WHITE:
        return (255, 255, 255)
    elif color==BLUE:
        return (0, 0, 255)
    else:
        return (0, 0, 0)

def rgb_to_color(rgb):
    return hsv_to_color(rgb_to_hsv(rgb))

def image_to_color(im):
    return image_to_arr(im, rgb_to_color)



def find_blobs(arr, color=None, reverse=False):
    """Find connected components
    
    Returns a (lazy) sequence containing the connected components of 'arr'
    that have the given 'color'.  If 'color' is not given, all
    connected components with non-zero color are returned.  If 'reverse'
    is True, components are found starting from the bottom."""
    
    if not reverse:
        rows=range(len(arr))
    else:
        rows=range(len(arr)-1, -1, -1)
    
    done=set()
    for i in rows:
        for j in range(len(arr[0])):
            
            if ( ((i, j) in done) or
                 (color is None and arr[i][j]==0) or
                 (color is not None and arr[i][j]!=color) ):
                continue
            
            #We've found a new component:
            done.add((i, j))
            current=list([(i, j)])
            que=deque([(i, j)])
            while(que):
                i, j=que.popleft()
                for ii, jj in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
                    if   (ii>=0 and ii<len(arr) and jj>=0 and jj<len(arr[0]) and
                          (ii, jj) not in done and arr[i][j]==arr[ii][jj]):
                        done.add((ii, jj))
                        current.append((ii, jj))
                        que.append((ii, jj))
            yield current
    return

def find_closest_ball(cam, arr):
    for b in find_blobs(arr, color=RED, reverse=True):
        if isBall(cam, b):
            return b[0]         #TODO: convert to angles
    return None

def isBall(cam, blob):
    """Check if a list of pixels is a ball"""
    #TODO: check trig to see if size is reasonable
    return len(blob)>4




class VisionThread(threading.Thread):
    def __init__(self, cam):
        threading.Thread.__init__(self)
        self.cam=cam
        self.running=False
    
    def run(self):
        self.running=True
        while self.running:
            im=self.cam.get_image()
            im.thumbnail((150, 150), Image.ANTIALIAS)
            arr=image_to_color(im)
            
            self.closest_ball=find_closest_ball(self.cam, arr)



#5x slower than PIL's convolve function, but allows out-of-bounds values
def convolve3(arr, mat):
    imax=len(arr)
    jmax=len(arr[0])
    kmax=len(arr[0][0])
    res=[[ [0, 0, 0] for j in arr[0] ] for i in arr]
    for i in range(imax):
        for j in range(jmax):
            for ii in range(-1, 2):
                for jj in range(-1, 2):
                    for k in range(kmax):
                        res[i][j][k]+=arr[min(max(i+ii, 0), imax-1)][min(max(j+jj, 0), jmax-1)][k]*mat[ii][jj]
    return res

def find_edges(arr):
    res=[[ [0, 0, 0] for j in arr[0] ] for i in arr]
    one=convolve3(arr, [[-1, -2, -1], 
                       [ 0,  0,  0],
                       [ 1,  2,  1]])
    two=convolve3(arr, [[-1, 0, 1],
                       [-2, 0, 2],
                       [-1, 0, 1]])
    imax=len(arr)
    jmax=len(arr[0])
    kmax=len(arr[0][0])
    for i in range(imax):
        for j in range(jmax):
            for k in range(kmax):
                res[i][j][k]=math.trunc(math.sqrt(one[i][j][k]*one[i][j][k]+two[i][j][k]*two[i][j][k])+.5)
    return res




def save_image(arr, filename):
    arr_to_image(arr).save(filename)



