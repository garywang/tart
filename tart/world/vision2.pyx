from collections import deque
import math, time, threading, cv, multiprocessing, numpy
from tart.sensors.camera import WebCam
from tart import params
cimport numpy


#Colors
RED=1           #ball
WHITE=2         #wall
BLUE=3          #top of wall
YELLOW=4        #center wall
PURPLE=5        #5-point line
GREEN=6         #bin
GRAY=0          #everything else

def read_color_data():
    try:
        f=open("/home/maslab-team-5/Maslab/tart/tart/sensors/colors.dat", "r")
        global color_arr
        color_arr=numpy.load(f)
        f.close()
    except IOError:
        print "Unable to read colors.dat"
        print "Run color calibration!"

read_color_data()

def get_rgb_from_color(color):
    if color==RED:
        return (255, 0, 0)
    elif color==WHITE:
        return (255, 255, 255)
    elif color==BLUE:
        return (0, 0, 255)
    elif color==YELLOW:
        return (255, 255, 0)
    elif color==PURPLE:
        return (255, 0, 255)
    elif color==GREEN:
        return (0, 255, 0)
    elif color==GRAY:
        return (0, 0, 0)
    else:
        return (150, 120, 0)

def convert_to_colors(numpy.ndarray[numpy.uint8_t, ndim=3] im):
    global color_arr
    cdef numpy.ndarray[numpy.int8_t, ndim=3] color_arr2=color_arr
    cdef int height=im.shape[0], width=im.shape[1]
    cdef int i, j
    cdef numpy.ndarray[numpy.int8_t, ndim=2] colors=numpy.empty((height, width), dtype=numpy.int8)
    for i in range(height):
        for j in range(width):
            colors[i, j]=color_arr2[im[i, j, 0], im[i, j, 1], im[i, j, 2]]
    return colors
    
def convert_to_image(numpy.ndarray[numpy.int8_t, ndim=2] colors):
    cdef int height=colors.shape[0], width=colors.shape[1]
    rgb=cv.CreateImage((width, height), cv.IPL_DEPTH_32F, 3)
    for i in range(height):
        for j in range(width):
            rgb[i, j]=get_rgb_from_color(colors[i, j])
    cv.CvtColor(rgb, rgb, cv.CV_RGB2BGR)
    return rgb


def find_blobs(numpy.ndarray[numpy.int8_t, ndim=2] im, color=None, reverse=False):
    """Find connected components
    
    Returns a (lazy) sequence containing the connected components of 'arr'
    that have the given 'color'.  If 'color' is not given, all
    connected components with non-zero color are returned.  If 'reverse'
    is True, components are found starting from the bottom."""
    
    cdef int height=im.shape[0], width=im.shape[1]
    cdef int i, j, ii, jj, i2, j2
    
    if not reverse:
        rows=range(height)
    else:
        rows=range(height-1, -1, -1)
    
    done=set()
    arr=[]
    for i in rows:
        for j in range(width):
            
            if ( ((i, j) in done) or
                 (color is None and im[i, j]==0) or
                 (color is not None and im[i, j]!=color) ):
                continue
            
            #We've found a new component:
            done.add((i, j))
            current=list([(i, j)])
            que=deque([(i, j)])
            while(que):
                i2, j2=que.popleft()
                for ii, jj in [(i2-1, j2), (i2+1, j2), (i2, j2-1), (i2, j2+1)]:
                    if   (ii>=0 and ii<height and jj>=0 and jj<width and
                          (ii, jj) not in done and im[i2, j2]==im[ii, jj]):
                        done.add((ii, jj))
                        current.append((ii, jj))
                        que.append((ii, jj))
            arr.append(current)
    return arr

class VisionThread(threading.Thread): #Not used
    def __init__(self, map=None, debug=False):
        threading.Thread.__init__(self)
        parent_conn, child_conn = multiprocessing.Pipe()
        self.map=map
        self.pipe=parent_conn
        self.debug=debug
        self.proc=VisionProcess(pipe=child_conn, debug=debug)
        self.running=False
    
    def run(self):
        self.running=True
        self.proc.start()
        
        if self.map is not None:
            pos=self.map.get_pos()
        
        while self.running:
            while self.running and not self.pipe.poll(1):
                pass
            if not self.running:
                break
            
            data=self.pipe.recv()
            if self.debug:
                print data
            
            self.balls=data["balls"]
            if len(self.balls)>0:
                self.closest_ball=self.balls[0]
            else:
                self.closest_ball=None
            
            if self.map is not None:
                self.map.update_balls(pos, self.balls)
                pos=self.map.get_pos()
            
        if self.proc.is_alive():
            self.pipe.send(False)
    
    def stop(self):
        self.running=False

class VisionProcess(multiprocessing.Process):

    def __init__(self, pipe, debug=params.vision_debug):
        """Initializes the vision process.

        cam_info is a CameraInfo object, used to initialize the camera's physical location
        pipe is used to communicate with the other process
        debug enables the debug mode"""
        multiprocessing.Process.__init__(self)
        self.pipe=pipe
        self.debug=debug
        self.colors=None
        if self.debug:
            self.debug_thread=DebugThread(self)
    
    def run(self):
        read_color_data()
        self.cam=WebCam(wrapped=True)
        if self.debug:
            self.debug_thread.start()
        try:
            while self.pipe.poll() == False or self.pipe.recv() == True:
                im=self.cam.get_image()
                small_im=cv.CreateImage((im.width/2, im.height/2), cv.IPL_DEPTH_8U, 3)
                cv.PyrDown(im, small_im);
                smaller_im=cv.CreateImage((im.width/4, im.height/4), cv.IPL_DEPTH_8U, 3)
                cv.PyrDown(small_im, smaller_im);
                
                mat=numpy.asarray(cv.GetMat(smaller_im))
                
                colors=convert_to_colors(mat)
                
                balls=self.find_balls(colors, smaller_im)
                
                walls=self.find_walls(colors, smaller_im)
                
                self.pipe.send({"balls": balls, "walls": walls})
                self.colors=colors
                
                #time.sleep(0.01)
        except KeyboardInterrupt:
            pass
        finally:
            if self.debug:
                self.debug_thread.stop()
            self.cam.stop()
    
    def find_balls(self, colors, im):
        balls=[]
        for b in find_blobs(colors, color=RED, reverse=True):
            if self.is_ball(b, im):
                balls.append(self.cam.info.get_vector(b[0], im))
        return balls
    
    def is_ball(self, blob, im):
        """Check if a list of pixels is a ball"""
        size=self.cam.info.get_pixel_size(blob[0], im)*len(blob)
        return size>15 and size<45
    
    def find_walls(self, numpy.ndarray[numpy.int8_t, ndim=2] colors, im, numpy.int8_t color=YELLOW):
        cdef int height=colors.shape[0], width=colors.shape[1]
        cdef int i, j, i0
        cdef double dx, dy
        cdef numpy.int8_t blue=BLUE
        
        walls=[]
        
        for j in range(0, width, 10):
            i=height-1
            while i>=0 and colors[i, j]!=color: i-=1
            i0=i
            while i>=0 and colors[i, j]==color: i-=1
            while i>=0 and colors[i, j]!=blue: i-=1
            if i<0 or colors[i, j]!=blue:
                continue
            while i>=0 and colors[i, j]==blue: i-=1
            if i<0:
                continue
            bot=self.cam.info.get_vector((i0, j), im)
            top=self.cam.info.get_vector((i+1, j), im, height=15.24)
            dx=bot[0]-top[0]
            dy=bot[1]-top[1]
            if dx*dx-dy*dy<4.:
                walls.append(bot)
        
        return walls

class DebugThread(threading.Thread):
    """Pretty colors"""
    def __init__(self, proc):
        threading.Thread.__init__(self)
        self.proc=proc
        self.running=False
    
    def run(self):
        self.running=True
        while self.proc.colors is None:
            time.sleep(0.01)
        while self.running:
            show_image(convert_to_image(self.proc.colors))
            time.sleep(0.05)
    
    def stop(self):
        self.running=False


def show_image(im, name="foo", num=1):
    for i in range(num):
        cv.ShowImage(name, im)
        cv.WaitKey(10)
