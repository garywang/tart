import time, sys
sys.path.append("/home/maslab-team-5/Maslab/tart/")
from tart.sensors import mouse

if __name__=="__main__":
    try:
        mouse=mouse.Mouse(0)
        while True:
            print mouse.speed, mouse.total
            time.sleep(0.01)
    except KeyboardInterrupt:
        print "Ending Program"
    
    finally:
        mouse.stop()

