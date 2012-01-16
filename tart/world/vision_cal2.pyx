import numpy, cv, threading, sys, time, pickle, Tkinter
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
from tart.sensors import camera, vision
cimport numpy

def get_hsv_from_rgb(int rr, int gg, int bb):
    cdef double r, g, b
    r, g, b=rr/255., gg/255., bb/255.
    cdef double delta, h, s, v
    
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
cdef numpy.int8_t RED=1           #ball
cdef numpy.int8_t WHITE=2         #wall
cdef numpy.int8_t BLUE=3          #top of wall
cdef numpy.int8_t YELLOW=4        #center wall
cdef numpy.int8_t PURPLE=5        #5-point line
cdef numpy.int8_t GREEN=6         #bin

cdef numpy.int8_t GRAY=0          #sat too low
cdef numpy.int8_t BLACK=7        #val too low
cdef numpy.int8_t OTHER=8        #unknown hue

white_sat_max=0.35
white_val_min=0.7
color_sat_min=0.4
color_val_min=0.1

def set_white_sat_max(val):
    global white_sat_max
    white_sat_max=float(val)

def set_white_val_min(val):
    global white_val_min
    white_val_min=float(val)

def set_color_sat_min(val):
    global color_sat_min
    color_sat_min=float(val)

def set_color_val_min(val):
    global color_val_min
    color_val_min=float(val)


cdef numpy.int8_t get_color_from_hsv(hsv):
    cdef double h, s, v
    h, s, v=hsv
    if s<white_sat_max and v>white_val_min:
        return WHITE
    elif v<color_val_min:
        return BLACK
    elif s<color_sat_min:
        return GRAY
    elif h>340 or h<20:
        return RED
    elif h<260 and h>170:
        return BLUE
    else:
        return OTHER

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
        return (64, 64, 64)
    elif color==BLACK:
        return (0, 0, 0)
    else:
        return (75, 60, 0)

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
    rgb=cv.CreateImage((colors.width, colors.height), cv.IPL_DEPTH_8U, 3)
    for i in range(colors.height):
        for j in range(colors.width):
            rgb[i, j]=get_rgb_from_color(colors[i, j])
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
            cv.PyrDown(im, small_im)
            smaller_im=cv.CreateImage((im.width/4, im.height/4), cv.IPL_DEPTH_8U, 3)
            cv.PyrDown(small_im, smaller_im)
            self.colors=convert_to_colors(smaller_im)
            vision.show_image(convert_to_image(self.colors))
            time.sleep(0.05)
        self.cam.stop()
    
    def stop(self):
        self.running=False

def calibrate():
    cam=camera.WebCam()
    global thr
    thr=ShowImageThread(cam)
    thr.start()
    
    global root
    root=Tkinter.Tk()
    
    Tkinter.Label(root, text="Black").grid(row=0, column=0)
    sc4=Tkinter.Scale(root, command=set_color_val_min, from_=0., to=1., resolution=0.01)
    sc4.set(color_val_min)
    sc4.grid(row=1, column=0)
    Tkinter.Label(root, text="Color").grid(row=1, column=1)
    sc2=Tkinter.Scale(root, command=set_white_val_min, from_=0., to=1., resolution=0.01)
    sc2.set(white_val_min)
    sc2.grid(row=1, column=2)
    Tkinter.Label(root, text="White").grid(row=2, column=2)
    
    Tkinter.Label(root).grid(row=3, column=0)
    
    Tkinter.Label(root, text="White").grid(row=4, column=0)
    sc1=Tkinter.Scale(root, command=set_white_sat_max, from_=0., to=1., resolution=0.01)
    sc1.set(white_sat_max)
    sc1.grid(row=5, column=0)
    Tkinter.Label(root, text="Gray").grid(row=6, column=0)
    Tkinter.Label(root, text="Gray").grid(row=4, column=2)
    sc3=Tkinter.Scale(root, command=set_color_sat_min, from_=0., to=1., resolution=0.01)
    sc3.set(color_sat_min)
    sc3.grid(row=5, column=2)
    Tkinter.Label(root, text="Color").grid(row=6, column=2)
    
    Tkinter.Button(root, text="Done", command=done).grid(row=7, column=1)
    
    root.mainloop()
    cancel()

def done():
    thr.stop()
    global BLACK
    global OTHER
    BLACK=GRAY
    OTHER=GRAY
    cdef numpy.ndarray[numpy.int8_t, ndim=3] color_arr=numpy.empty((256, 256, 256), dtype=numpy.int8)
    cdef int r, g, b
    for r in xrange(256):
        for g in xrange(256):
            for b in xrange(256):
                color_arr[r, g, b]=get_color_from_hsv(get_hsv_from_rgb(b, g, r))
        print r
    f=open("/home/maslab-team-5/Maslab/tart/tart/sensors/colors.dat", "w")
    numpy.save(f, color_arr)
    f.close()
    root.quit()

def cancel():
    thr.stop()
