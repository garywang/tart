"""Contain constants and calibration values for everything else"""

import sys, math
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
from tart.world.trig import CameraInfo

#Use WrappedCamera
webcam_wrapped=True
#Physical information about camera
webcam_info=CameraInfo(cam_height=29., height_angle=0.70, width_angle=0.93, min_dist=28.)
#Camera number (0 or 1)
webcam_num=1

#Show colored image from camera on screen
vision_debug=False

#Number of mouse ticks per centimeter
mouse_scale=160.

#Mouse numbers (0, 1, or 2)
odometry_num1=1
odometry_num2=2
#Half the distance between the mice, in cm
odometry_radius=3.2
#Time, in seconds, over which to calculate mouse velocities
odometry_interval=0.04

#Show map on screen
mapping_debug=False
#Balls within this angle are forgotten if not in current image
mapping_mem_width=0.4

#Print state names
state_debug=False
#Speed robot turns at when scanning for balls
state_scan_speed=50
#Maximum extra angle that robot rotates after completing full circle
state_scan_angle_max=math.pi
#Distance, in cm, that causes robot to enter CaptureState
state_capture_dist=40
#Robot will not enter CaptureState if angle to ball is greater than this
state_capture_max_angle=0.1
#Time, in seconds, that causes robot to leave CaptureState
state_capture_timeout=4
#Distance, in cm, that causes robot to leave CaptureState
state_capture_exit_dist=5
#Time, in seconds, that robot stays in ExploreState
state_explore_timeout=5

#Print target of driving
drive_debug=False
#PID parameters for drive_to_point
drive_drive_kp=100
#PID parameters for rotate_toward_point
drive_rotate_kp=100

#Motor controller and motor numbers of omniwheels
omni_l=(1, 0)
omni_r=(1, 1)
omni_b=(2, 0)
