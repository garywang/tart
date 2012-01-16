import numpy, cv, threading, sys, time, pickle
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
from tart.sensors import camera
from tart.world import vision

def get_hsv_from_rgb(rgb):
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

white_sat_max=0.35
white_val_min=0.7
color_sat_min=0.4
color_val_min=0.1

def get_color_from_hsv(hsv):
    h, s, v=hsv
    if s<white_sat_max and v>white_val_min:
        return WHITE
    elif s<color_sat_min or v<color_val_min:
        return GRAY
    elif h>340 or h<20:
        return RED
    elif h<260 and h>170:
        return BLUE
    else:
        return GRAY

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
            rgb[i, j]=vision.get_rgb_from_color(colors[i, j])
    cv.CvtColor(rgb, rgb, cv.CV_RGB2BGR)
    return rgb


class ShowImageThread(threading.Thread):
    
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
            vision.show_image(convert_to_image(convert_to_colors(smaller_im)))
            time.sleep(0.05)
        self.cam.stop()
    
    def stop(self):
        self.running=False

def calibrate():
    cam=camera.WebCam()
    global thr
    thr=ShowImageThread(cam)
    thr.start()
    print "Type done() when done"

def done():
    thr.stop()
    color_arr=numpy.empty((256, 256, 256), dtype=numpy.int8)
    for r in xrange(256):
        for g in xrange(256):
            for b in xrange(256):
                color_arr[r, g, b]=get_color_from_hsv(get_hsv_from_rgb((b, g, r)))
        print r
    f=open("/home/maslab-team-5/Maslab/tart/tart/sensors/colors.dat", "w")
    numpy.save(f, color_arr)
    f.close()
    exit()

def cancel():
    thr.stop()
    exit()

if __name__=="__main__":
    calibrate()
