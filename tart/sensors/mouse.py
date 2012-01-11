import threading, time
from collections import deque

class Mouse(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.mouse=open("/dev/input/mouse"+str(num), "r")
        self.pos=(0, 0)
        self.sumx=0
        self.sumy=0
        self.d=deque()
        self.interval=0.04
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
            self.sumx+=x
            self.sumy+=y
            self.d.append((time.time(), x, y))
            self.pos=(self.pos[0]+x, self.pos[1]+y)
    
    def get_speed(self):
        t=time.time()
        while len(self.d)>0 and t-self.d[0][0]>self.interval:
            self.sumx-=self.d[0][1]
            self.sumy-=self.d[0][2]
            self.d.popleft()
        return (self.sumx/self.interval, self.sumy/self.interval)
    
    def get_pos(self):
        return self.pos
    
    def stop(self):
        self.running=False
