import sys, pyximport; pyximport.install()
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
from tart.world import vision_cal2 as cal

if __name__=="__main__":
    cal.calibrate()
