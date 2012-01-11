import threading, time
from collections import deque

class Mouse(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.mouse=open("/dev/input/mouse"+str(num), "r")
        self.start()
    
    def run(self):
        self.running=True
        self.speed=(0, 0)
        self.total=(0, 0)
        sumx=0
        sumy=0
        d=deque()
        interval=0.04
        while self.running:
            s=self.mouse.read(3)
            x, y=ord(s[1]), ord(s[2])
            if ord(s[0])&16>0:
                x-=256
            if ord(s[0])&32>0:
                y-=256
            sumx+=x
            sumy+=y
            t=time.time()
            d.append((t, x, y))
            while t-d[0][0]>interval:
                sumx-=d[0][1]
                sumy-=d[0][2]
                d.popleft()
            self.speed=(sumx/interval, sumy/interval)
            self.total=(self.total[0]+x, self.total[1]+y)
    
    def stop(self):
        self.running=False
