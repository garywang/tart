import time, sys
sys.path.append("/home/maslab-team-5/Maslab/tart/")
from tart.sensors.mouse import Mouse

if __name__=="__main__":
    try:
        mouse=Mouse(0)
        while True:
            print mouse.speed, mouse.total
            time.sleep(0.01)
    except KeyboardInterrupt:
        print "Ending Program"
    
    finally:
        mouse.stop()

