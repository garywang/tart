import sys, time, math
import threading, thread
from tart.actuators import drive
from tart.sensors import sensor
from tart import params

class WallFollowController:
    def __init__(self, ard, drive, back_port=8, side_port=9):
        """Follows a wall.
        
        Takes port numbers for two short IR sensors: back, facing the back of the robot; and side, facing 45 degrees from the back."""
        self.drive = drive
        self.back = sensors.ShortIR(ard, back_port)
        self.side = sensors.ShortIR(ard, side_port)
        self.wall = False

    def follow_wall(self):
        """Uses a simple form of control to follow walls.
        
        If its back is to a wall, it translates rightward along the wall. Otherwise, it drives backward until it hits a wall."""
        if self.at_wall():
            self.track_wall()
        else:
            self.find_wall()

    def at_wall(self):
        back_dist = self.back.get_dist()
        side_dist = self.side.get_dist()
        if min(back_dist, side_dist) < 15: # Found a wall
            self.wall = True
        elif min(back_dist, side_dist) > 30: # Lost the wall
            self.wall = False
        return self.wall

    def track_wall(self):
        side_dist = self.side.get_dist()
        if side_dist < 25: # Too close
            self.drive.rotate(-30)
        elif side_dist > 30: # Too far
            self.drive.rotate(30)
        else:
            self.drive.translate(127, 70)

    def find_wall(self): # Possibly might need to be more involved.
        self.drive.translate(127, 180)
