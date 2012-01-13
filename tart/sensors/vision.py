from collections import deque
import math, time, threading, cv, multiprocessing, numpy
from tart.sensors.camera import WebCam


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
    else:
        return (0, 0, 0)

def convert_to_colors(im):
    global color_arr
    colors=cv.CreateImage((im.width, im.height), cv.IPL_DEPTH_8U, 1)
    for i in xrange(im.height):
        for j in xrange(im.width):
            colors[i, j]=color_arr[im[i, j]]
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
    def __init__(self, info=None, debug=False):
        threading.Thread.__init__(self)
        parent_conn, child_conn = multiprocessing.Pipe()
        self.pipe=parent_conn
        self.proc=VisionProc(info, child_conn, debug)
        self.running=False
    
    def run(self):
        self.running=True
        self.proc.start()
        while self.running:
            self.pipe.send(True)
            while self.running and not self.pipe.poll(1):
                pass
            if not self.running:
                break
            data=self.pipe.recv()
            print data
            self.closest_ball=data["closest_ball"]
        print "foo"
        if self.proc.is_alive():
            self.pipe.send(False)
    
    def stop(self):
        self.running=False

class VisionProc(multiprocessing.Process):
    def __init__(self, cam_info, pipe, debug=False):
        multiprocessing.Process.__init__(self)
        self.cam_info=cam_info
        self.pipe=pipe
        self.debug=debug
        if self.debug:
            self.debug_thread=DebugThread(self)
    
    def run(self):
        read_color_data()
        self.cam=WebCam(info=self.cam_info)
        if self.debug:
            self.debug_thread.start()
        try:
            while self.pipe.recv() == True:
                im=self.cam.get_image()
                small_im=cv.CreateImage((im.width/2, im.height/2), cv.IPL_DEPTH_8U, 3)
                cv.PyrDown(im, small_im);
                smaller_im=cv.CreateImage((im.width/4, im.height/4), cv.IPL_DEPTH_8U, 3)
                cv.PyrDown(small_im, smaller_im);
                smallerer_im=cv.CreateImage((im.width/8, im.height/8), cv.IPL_DEPTH_8U, 3)
                cv.PyrDown(smaller_im, smallerer_im);
                
                colors=convert_to_colors(smallerer_im)
                
                closest_ball=self.find_closest_ball(colors)
                
                self.pipe.send({"closest_ball": closest_ball})
                self.colors=colors
                
                #time.sleep(0.01)
        except KeyboardInterrupt:
            pass
        finally:
            if self.debug:
                self.debug_thread.stop()
            self.cam.stop()
    
    def find_closest_ball(self, im):
        for b in find_blobs(im, color=RED, reverse=True):
            if self.is_ball(b, im):
                return self.cam.info.get_vector(b[0], im)
        return None
    
    def is_ball(self, blob, im):
        """Check if a list of pixels is a ball"""
        size=self.cam.info.get_pixel_size(blob[0], im)*len(blob)
        return size>15 and size<45

class DebugThread(threading.Thread):
    
    def __init__(self, proc):
        threading.Thread.__init__(self)
        self.proc=proc
        self.running=False
    
    def run(self):
        self.running=True
        time.sleep(1)
        while self.running:
            show_image(convert_to_image(self.proc.colors))
            time.sleep(0.05)
    
    def stop(self):
        self.running=False


def show_image(im, name="foo", num=1):
    for i in range(num):
        cv.ShowImage(name, im)
        cv.WaitKey(10)
