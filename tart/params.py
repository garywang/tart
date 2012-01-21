"""Contain constants and calibration values for everything else"""

import sys
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
from tart.world.trig import CameraInfo

webcam_wrapped=True
webcam_info=CameraInfo(cam_height=29., height_angle=0.70, width_angle=0.93, min_dist=28.)
webcam_num=1

vision_debug=False

odometry_num1=1
odometry_num2=2
odometry_radius=3.2

mapping_debug=False

