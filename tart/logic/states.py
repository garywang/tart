import time, math, random
robot = None

class State:
    """Base class for state machine states

    Does things common to all states"""
    
    def __init__(self):
        self.map=robot.map
        self.drive=robot.drive
        self.start_time=time.time()
    
    def step(self):
        """Run one iteration of the state, return the next state"""
        # stuff common to all states?
        return self

class ScanState(State):
    """Scan the field until we see a ball. Then enter ApproachState"""
    def __init__(self):
        State.__init__(self)
        if self.map.get_velocity()[2]>0:
            self.dir=-1
        else:
            self.dir=1
        self.start_angle = self.map.get_pos()[2]
        self.angle_duration = random.uniform(2*math.pi, 5*math.pi/2)
    
    def step(self):
        if self.map.get_visible_ball(): # sees a ball
            return ApproachState()
        if math.fabs(self.map.get_pos()[2] - self.start_angle) > self.angle_duration:
            return ExploreState()
        
        self.drive.rotate(self.dir*50)
        return self

class RememberState(State):
    """Turn toward a ball that was seen before"""
    
    def step(self):
        if self.map.get_visible_ball():
            return ApproachState()
        ball=self.map.get_memorized_ball()
        if ball is None:
            return ScanState()
        self.drive.rotate_toward_point(ball)
        return self

class ApproachState(State):
    """Approaches a ball."""
    
    def step(self):
        ball=self.map.get_visible_ball()
        if ball is None:
            return RememberState()
        vec=self.map.get_vector_to(ball)
        if vec[1]<40.:
            if math.fabs(math.atan2(vec[1], vec[0])-math.pi/2)<0.1:
                return CaptureState(ball)
            self.drive.rotate_toward_point(ball)
        else:
            self.drive.drive_to_point(ball)
        return self

class CaptureState(State):
    """Captures a ball"""
    def __init__(self, ball):
        State.__init__(self)
        self.ball = ball
    
    def step(self):
        self.drive.drive_to_point(self.ball)
        if self.map.get_length(self.map.get_vector_to(self.ball))<5 or \
                time.time()-self.start_time>4:
            return RememberState()
        else:
            return self

class ExploreState(State):
    """Go somewhere else so it can see some balls"""
    
    def step(self):
        if self.map.get_closest_ball():
            return ApproachState()
        if time.time()-self.start_time>5:
            return ScanState()
        self.drive.forward()
        return self
