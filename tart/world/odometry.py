import threading, time, math
from collections import deque
from tart.sensors.mouse import Mouse
from tart import params

class OdometryThread(threading.Thread):

    def __init__(self, num1=params.odometry_num1, num2=params.odometry_num2, radius=params.odometry_radius):
        threading.Thread.__init__(self)
        self.m1=Mouse(num1)
        self.m2=Mouse(num2)
        self.radius=radius
        self.x=0.
        self.y=0.
        self.theta=0.
        self.interval=params.odometry_interval
        self.que=deque()
        self.running=False
    
    def run(self):
        self.running=True
        self.m1.get_delta()
        self.m2.get_delta()
        while self.running:
            x1, y1=self.m1.get_delta()
            x2, y2=self.m2.get_delta()
            dx=(x1+x2)/2.
            dy=(y1+y2)/2.
            self.x+=dx*math.cos(self.theta)-dy*math.sin(self.theta)
            self.y+=dx*math.sin(self.theta)+dy*math.cos(self.theta)
            self.theta+=(y2-y1)/(2.*self.radius)
            self.que.append((time.time(), self.x, self.y, self.theta))
        self.m1.stop()
        self.m2.stop()
    
    def get_pos(self):
        return (self.x, self.y, self.theta)
    
    def get_speed(self):
        t=time.time()
        while len(self.que)>0 and t-self.que[0][0]>self.interval:
            self.que.popleft()
        if len(self.que)>1:
            one=self.que[0]
            two=self.que[-1]
            dt=two[0]-one[0]
            return ((two[1]-one[1])/dt, (two[2]-one[2])/dt, (two[3]-one[3])/dt)
        return (0., 0., 0.)
    
    def stop(self):
        self.running=False

