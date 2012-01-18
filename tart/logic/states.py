robot = None

class State:
    """Base class for state machine states

    Does things common to all states"""

    def step(self):
        "Run one iteration of the state, return the next state"
        # stuff common to all states?
        return self

class ScanState(State):
    """Scan the field until we see a ball. Then enter ApproachState"""
    def __init__(self):
        self.map = robot.map
        self.drive = robot.drive
        self.start_angle = self.map.get_pos()[2]

    def step(self):
        if self.map.get_closest_ball(): # sees a ball
            return ApproachState()
        if self.map.get_pos()[2] - self.start_angle > 2*math.pi: # rotated 360
            return ExploreState()

        self.drive.rotate(50)
        return self
    
class RememberState(State):
    """Turn toward a ball that was seen before"""
    def __init__(self):
        pass

    def step(self):
        return ScanState()

class ApproachState(State):
    """Approaches a ball."""
    def __init__(self):
        self.map = robot.map
        self.drive = robot.drive

    def step(self):
        if self.map.get_closest_ball() is None:
            return RememberState()
        if False: ###within certain distance
            # remember ball location? pass it to capturestate?
            return CaptureState()
        #x, y = self.map.get_vector_to(self.map.get_closest_ball())
        # this stuff should go in control eventually.
        #angle=math.pi/2-atan2(y, x)     #Right is positive, left is negative
        #self.drive.forward(rotation=angle*100)
        self.drive.drive_to_point(map.get_visible_ball())
        return self

class CaptureState(State):
    """Captures a ball"""
    def __init__(self, ball):
        self.ball = ball

    def step(self):

        return RememberState()

class ExploreState(State):
    """Go somewhere else so it can see some balls"""
    def __init__(self):
        self.drive = robot.drive

    def step(self):
        if self.map.get_closest_ball():
            return ApproachState()

        return self
