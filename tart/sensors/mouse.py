import threading, sys
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
from tart import params

class Mouse(threading.Thread):
    def __init__(self, num, scale=params.mouse_scale):
        threading.Thread.__init__(self)
        self.mouse=open("/dev/input/mouse"+str(num), "r")
        self.scale=scale+0.
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
            self.sumx+=x/self.scale
            self.sumy+=y/self.scale
            self.lock.release()
    
    def get_delta(self):
        self.lock.acquire()
        res=(-self.sumx, -self.sumy)
        self.sumx=0
        self.sumy=0
        self.lock.release()
        return res
    
    def stop(self):
        self.running=False
