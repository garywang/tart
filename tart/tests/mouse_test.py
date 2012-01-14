import time, sys
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
from tart.sensors.mouse import OdometryThread

if __name__=="__main__":
    try:
        mice=OdometryThread(0, 1, 3.2)
        mice.start()
        while True:
            print mice.get_speed(), mice.get_pos()
            time.sleep(0.01)
    except KeyboardInterrupt:
        print "Ending Program"
    
    finally:
        mice.stop()

