import sys, pyximport; pyximport.install()
import math, threading, multiprocessing, cv
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
from tart.world import vision2 as vision
from tart.world import odometry

class Map(threading.Thread):
    
    def __init__(self, odom=True, debug=False):
        threading.Thread.__init__(self)
        #self.vis=vision.VisionThread(map=self)
        parent_conn, child_conn = multiprocessing.Pipe()
        self.vis_pipe = parent_conn
        self.vis_proc = vision.VisionProcess(child_conn)
        if odom:
            self.odometry = odometry.OdometryThread()
        self.closest_ball = None
        self.memorized_balls = []
        self.debug = debug
        if self.debug:
            self.debug_thread=MapDisplayThread(self)
        self.running = False
    
    def run(self):
        self.running = True
        self.vis_proc.start()
        if self.odometry:
            self.odometry.start()
        
        if self.debug:
            self.debug_thread.start()
        
        pos = self.get_pos()

        while self.running:
            if not self.vis_pipe.poll(): # no updates from vision
                continue

            data = self.vis_pipe.recv()
            if self.debug:
                print data
            
            self.update_balls(pos, data["balls"])
            pos = self.get_pos()
    
    def stop(self):
        self.running = False
        if self.odometry:
            self.odometry.stop()
        if self.vis_proc.is_alive():
            self.vis_pipe.send(False)
        if self.debug:
            self.debug_thread.stop()
    
    def update_balls(self, pos, balls):
        for ball in balls:
            ball=self.get_abs_loc(vec=ball, rel=pos)
        if len(balls)==0:
            self.closest_ball=None
        else:
            self.closest_ball=balls[0]
        for ball in self.memorized_balls:
            if math.fabs(self.get_angle(self.get_vector_to(loc=ball, rel=pos))) > 0.3:
                balls.append(ball)
        self.memorized_balls=balls
        if self.debug:
            print str(len(self.memorized_balls))+" memorized balls"
    
    def get_pos(self):
        """Get current position (x, y, theta)"""
        if self.odometry:
            return self.odometry.get_pos()
        else:
            return (0, 0, 0)
    
    def get_velocity(self):
        """Get current velocity (vx, vy, vtheta)"""
        if self.odometry:
            return self.odometry.get_speed()
        else:
            return (0, 0, 0)
    
    def get_abs_loc(self, vec, rel=None):
        """Get absolute location (x, y) of vec relative to current position or rel"""
        if rel is None:
            rel=self.get_pos()
        dx, dy=vec[0:2]
        x0, y0, theta=rel
        return (x0+dx*math.cos(theta)-dy*math.sin(theta), \
                y0+dx*math.sin(theta)+dy*math.cos(theta))
    
    def get_vector_to(self, loc, rel=None):
        """Get vector (dx, dy) to loc from current position or rel"""
        if rel is None:
            rel=self.get_pos()
        x0, y0, theta=rel
        x, y=loc[0:2]
        dx=x-x0
        dy=y-y0
        return (dx*math.cos(theta)+dy*math.sin(theta), \
               -dx*math.sin(theta)+dy*math.cos(theta))
    
    def get_length(self, vec):
        """Return length of vec (x, y)"""
        x, y=vec
        return math.sqrt(x*x+y*y)
    
    def get_angle(self, vec):
        """Return angle to vec (x, y)"""
        x, y = vec
        return math.pi/2 - math.atan2(y, x)
   
    def get_visible_ball(self):
        """Return absolute location (x, y) of closest ball"""
        return self.closest_ball
    
    def get_memorized_ball(self):
        """Return memorized ball with smallest angle to current orientation"""
        best=None
        best_angle=math.pi
        for ball in self.memorized_balls:
            v = self.get_vector_to(ball)
            if math.fabs(self.get_angle(v))<best_angle:
                best_angle=math.fabs(self.get_angle(v))
                best=ball
        return best

class MapDisplayThread(threading.Thread):
    def __init__(self, map):
        threading.Thread.__init__(self)
        self.map=map
        self.running=False
    
    def run(self):
        self.running=True
        im=cv.CreateImage((500, 500), cv.IPL_DEPTH_8U, 3)
        while self.running:
            cv.Rectangle(im, (0,0), (500,500), (255, 255, 255), cv.CV_FILLED)
            cv.Circle(im, self.get_pixel(self.map.get_pos()), 8, (0, 0, 0), cv.CV_FILLED)
            cv.Line(im, self.get_pixel(self.map.get_abs_loc((0, -15))), \
                        self.get_pixel(self.map.get_abs_loc((0, 15))), (255, 255, 255))
            cv.Line(im, self.get_pixel(self.map.get_abs_loc((0, 15))), \
                        self.get_pixel(self.map.get_abs_loc((15, 0))), (255, 255, 255))
            cv.Line(im, self.get_pixel(self.map.get_abs_loc((0, 15))), \
                        self.get_pixel(self.map.get_abs_loc((-15, 0))), (255, 255, 255))
            for ball in self.map.memorized_balls:
                cv.Circle(im, self.get_pixel(ball), 2, (0, 0, 155), cv.CV_FILLED)
            cur_ball=self.map.get_visible_ball() or self.map.get_memorized_ball()
            if cur_ball is not None:
                cv.Circle(im, self.get_pixel(cur_ball), 2, (0, 0, 255), cv.CV_FILLED)
            cv.ShowImage("map", im)
            cv.WaitKey(20)
    
    def get_pixel(self, pos):
        return (int(pos[0]/2.+250), int(pos[1]/2.+250))
    
    def stop():
        self.running=False
