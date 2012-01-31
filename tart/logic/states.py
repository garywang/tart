import time, math, random, sys
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
from tart import params
robot = None
stuck_detect = None

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
        return self or stuck_detect.detect()

class ScanState(State):
    """Scan the field until we see a ball. Then enter ApproachState"""
    def __init__(self):
        State.__init__(self)
        if self.map.get_velocity()[2]>0:
            self.dir=-1
        else:
            self.dir=1
        self.start_angle = self.map.get_pos()[2]
        self.angle_duration = random.uniform(2*math.pi, 2*math.pi+params.state_scan_angle_max)
    
    def step(self):
        if robot.get_time()>params.state_approach_yellow_time:
            if self.map.get_memorized_wall():
                return ApproachYellowState()
        elif self.map.get_visible_ball(): # sees a ball
            return ApproachState()
        
        if math.fabs(self.map.get_pos()[2] - self.start_angle) > self.angle_duration:
            if robot.get_time()>params.state_find_yellow_time:
                wall=self.map.get_memorized_wall()
                if wall is not None and \
                        self.map.get_length(self.map.get_vector_to(wall))>params.state_find_yellow_dist:
                    return ExploreYellowState()
            return ExploreState()
        
        self.drive.rotate(self.dir*params.state_scan_speed)
        return stuck_detect.detect() or self

class RememberState(State):
    """Turn toward a ball that was seen before"""
    
    def step(self):
        if robot.get_time()>params.state_approach_yellow_time:
            return ScanState()
        if self.map.get_visible_ball():
            return ApproachState()
        ball=self.map.get_memorized_ball()
        if ball is None:
            return ScanState()
        self.drive.rotate_toward_point(ball)
        return stuck_detect.detect() or self

class ApproachState(State):
    """Approaches a ball."""
    
    def step(self):
        if robot.get_time()>params.state_approach_yellow_time:
            return ScanState()
        ball=self.map.get_visible_ball()
        if ball is None:
            return RememberState()
        vec=self.map.get_vector_to(ball)
        if vec[1]<params.state_capture_dist:
            if math.fabs(math.atan2(vec[1], vec[0])-math.pi/2)<params.state_capture_max_angle:
                return CaptureState(ball)
            self.drive.rotate_toward_point(ball)
        else:
            self.drive.drive_to_point(ball)
        return stuck_detect.detect() or self

class CaptureState(State):
    """Captures a ball"""
    def __init__(self, ball):
        State.__init__(self)
        self.ball = ball
    
    def step(self):
        self.drive.drive_to_point(self.ball)
        if self.map.get_length(self.map.get_vector_to(self.ball))<params.state_capture_exit_dist or \
                time.time()-self.start_time>params.state_capture_timeout:
            return RememberState()
        else:
            return stuck_detect.detect() or self

class ExploreState(State):
    """Go somewhere else so it can see some balls"""
    
    def step(self):
        if self.map.get_visible_ball():
            return ApproachState()
        if time.time()-self.start_time>params.state_explore_timeout:
            return ScanState()
        self.drive.forward()
        return stuck_detect.detect() or self

class ExploreYellowState(State):
    """Go within some distance of the yellow wall"""
    
    def step(self):
        if self.map.get_visible_ball():
            return ApproachState()
        if time.time()-self.start_time>params.state_explore_timeout:
            return ScanState()
        wall=self.map.get_memorized_wall()
        if wall is not None and \
                self.map.get_length(self.map.get_vector_to(wall))>2*params.state_find_yellow_dist/3:
            self.drive.drive_to_point(wall)
            return stuck_detect.detect() or self
        return ScanState()

class ApproachYellowState(State):
    """Approach yellow wall"""
    
    def step(self):
        wall=self.map.get_memorized_wall()
        if wall is None:
            return ScanState()
        vec=self.map.get_vector_to(wall)
        if vec[1]<params.state_capture_dist:
            if math.fabs(math.atan2(vec[1], vec[0])-math.pi/2)<params.state_capture_max_angle:
                return CaptureYellowState(wall)
            self.drive.rotate_toward_point(wall)
        else:
            self.drive.drive_to_point(wall)
        return stuck_detect.detect() or self

class CaptureYellowState(State):
    """Drive up to yellow wall"""
    def __init__(self, wall):
        State.__init__(self)
        self.wall = wall
    
    def step(self):
        self.drive.drive_to_point(self.wall)
        #TODO: check bump sensors, launch catapult
        return self
