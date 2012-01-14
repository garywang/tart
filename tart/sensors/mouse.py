import threading, time, math
from collections import deque

class Mouse(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.mouse=open("/dev/input/mouse"+str(num), "r")
        self.sumx=0
        self.sumy=0
        self.lock=threading.Lock()
        self.start()
    
    def run(self):
        self.running=True
        while self.running:
            s=self.mouse.read(3)
            x, y=ord(s[1]), ord(s[2])
            if ord(s[0])&16>0:
                x-=256
            if ord(s[0])&32>0:
                y-=256
            self.lock.acquire()
            self.sumx+=x/160.
            self.sumy+=y/160.
            self.lock.release()
    
    def get_delta(self):
        self.lock.acquire()
        res=(self.sumx, self.sumy)
        self.sumx=0
        self.sumy=0
        self.lock.release()
        return res
    
    def stop(self):
        self.running=False
    

class OdometryThread(threading.Thread):

    def __init__(self, num1=1, num2=2, radius=256.):
        threading.Thread.__init__(self)
        self.m1=Mouse(num1)
        self.m2=Mouse(num2)
        self.radius=radius
        self.x=0.
        self.y=0.
        self.theta=0.
        self.interval=0.04
        self.que=deque()
        self.running=False
    
    def run(self):
        self.running=True
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
        return (0., 0., 123.)
    
    def stop(self):
        self.running=False

