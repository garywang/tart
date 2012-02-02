"""Contain constants and calibration values for everything else"""

import sys, math
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
from tart.world.trig import CameraInfo

#Use WrappedCamera
webcam_wrapped=True
#Physical information about camera
webcam_info=CameraInfo(cam_height=18., height_angle=0.70, width_angle=0.93, min_dist=18.)
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
odometry_radius=7.75
#Time, in seconds, over which to calculate mouse velocities
odometry_interval=0.04

#Show map on screen
mapping_debug=True
#Balls within this angle are forgotten if not in current image
mapping_mem_width=0.45
mapping_odom=True

#Print state names
state_debug=True
#Speed robot turns at when scanning for balls
state_scan_speed=50
#Maximum extra angle that robot rotates after completing full circle
state_scan_angle_max=math.pi
#Distance, in cm, that causes robot to enter CaptureState
state_capture_dist=25
#Robot will not enter CaptureState if angle to ball is greater than this
state_capture_max_angle=0.1
#Time, in seconds, that causes robot to leave CaptureState
state_capture_timeout=4
#Distance, in cm, that causes robot to leave CaptureState
state_capture_exit_dist=5
#Time, in seconds, that robot stays in ExploreState
state_explore_timeout=5
#Time, in seconds, after which the robot will move closer to the yellow wall
#if it can't find a ball
state_explore_yellow_time=120
#Distance, in cm, from the yellow wall that the robot moves to in FindYellowState
state_explore_yellow_dist=150
#Time, in seconds, after which the robot will try to enter ApproachYellowState
state_approach_yellow_time=150

#Print target of driving
drive_debug=True
#PID parameters for drive_to_point
drive_drive_kp=100
#PID parameters for rotate_toward_point
drive_rotate_kp=100

#Motor controller and motor numbers of omniwheels
omni_l=(24, 25, 3)
omni_r=(26, 27, 4)
omni_b=(22, 23, 2)

#Print commands sent/received from Arduino
arduino_debug=False

