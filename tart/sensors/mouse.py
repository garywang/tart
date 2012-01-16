import threading

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
