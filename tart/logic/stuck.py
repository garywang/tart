import time, math, random, sys
from collections import deque
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
from tart import params
from tart.logic.states import State, ExploreState
robot = None

class StuckDetector:
    
    def __init__(self, _robot):
        #self.long_que=deque()
        self.short_que=deque()
        self.map=_robot.map
        self.robot=_robot
        global robot
        robot=_robot
    
    def detect(self):
        pos=self.map.get_pos()
        #self.long_que.append((time.time(), pos))
        self.short_que.append((time.time(), pos))
        last=None
        print len(self.short_que)
        while time.time()-self.short_que[0][0]>5.:
            last=self.short_que.popleft()
        if last is not None and self.map.odometry is not None:
            d=self.get_delta(last[1])
            print d
            if d[0]<2. and d[1]<math.pi/12:
                return BackUpState()
        
        if time.time()-robot.sm.state.start_time>15.:
            return RotateState()
        
        return False
    
    def get_delta(self, one, two=None):
        if two is None:
            two=self.map.get_pos()
        return ( ((one[0]-two[0])**2+(one[1]-two[1])**2)**.5, \
                abs(one[2]-two[2]) )
        

class BackUpState(State):
    
    def __init__(self, theta=None):
        State.__init__(self)
        if theta is None:
            self.theta=math.pi
        else:
            self.theta=theta
        self.timeout=random.uniform(1.5, 3.)
    
    def step(self):
        self.drive.translate(127, math.degrees(self.theta))
        if time.time()-self.start_time<self.timeout:
            return self
        return RotateState()

class RotateState(State):
    
    def __init__(self):
        State.__init__(self)
        self.dir=random.choice([-1, 1])
        self.timeout=random.uniform(0.2, 1)
    
    def step(self):
        self.drive.rotate(self.dir*127)
        if time.time()-self.start_time<self.timeout:
            return self
        return ExploreState()#ForwardState()

class ForwardState(State):
    
    def __init__(self):
        State.__init__(self)
        self.start_pos=self.map.get_pos()
        self.timeout=2
    
    def step(self):
        self.drive.forward()
        if time.time()-self.start_time>self.timeout:
            return BackUpState(random.uniform(0, 2*math.pi))
        if self.map.get_length(self.map.get_vector_to(self.start_pos))<20:
            return self
        return ExploreState()
