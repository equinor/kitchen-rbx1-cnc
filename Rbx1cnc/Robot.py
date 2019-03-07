import RPi.GPIO as GPIO
import Slush
import threading
import signal
import math
import time
from .Axis import Axis, NullAxis

class Robot:
    def __init__(self):
        
        self._target = [0,0,0,0,0,0, 0]
        self._prevPos = [0,0,0,0,0,0, 0]
        self._speed = [10, 50, 30, 15, 10, 5]
        self._axis = []
        self._gripper = None
        # A running thread contineously keep track of target and current
        #  position and move robot accordingly
        self.thread = None
        self.killMover = False
        self.thread = threading.Thread(target=self._robotMoverThread)
        signal.signal(signal.SIGINT, self.handler)
        self.thread.start()

    def handler(self):
        if Robot.thread is not None:
            Robot.killMover = True

    def isBusy(self):
        for axis in self._axis:
            if axis.isBusy(): return True
        return False

    def kill(self):
        for axis in self._axis:
            if type(axis) is NullAxis: continue
            axis.getJoint().hardStop()
        self.killMover = True

    def setGoalTarget(self, points):
        self._target = points

    def getStatus(self): 
        pos = list(map(lambda a: a.getPosition(), self._axis))
        gripperPos = 0
        if self._gripper: gripperPos = self._gripper.getPosition()
        pos.append(gripperPos)
        return {
            'busy': self.isBusy(),
            'targetPos' : self._target,
            'currentPos' : pos
        }
  
    def runRobot(self):
        # Use the run command similar to the joystick example with manual stop and movement

        for i, axis in enumerate(self._axis):
            if type(axis) is NullAxis: continue
            joint = axis.getJoint()
            pos = joint.getPosition()
            # Filter out sudden big changes in position. Happens once in a while a gives 
            # the robots a sudden tick.
            if abs(pos - self._prevPos[i]) > 1000: continue
            self._prevPos[i] = pos
        
            correctedPos = min(max(axis._min, pos), axis._max)
            goalPos = axis._toStep(self._target[i])

            if goalPos > axis._max or goalPos < axis._min:
                joint.hardStop()
                continue
            
            diff = axis._toStep(self._target[i]) - correctedPos
            if abs(diff) > 0: print('p', pos, 'diff', diff)
            if not joint.isBusy():
                if abs(diff) < self._speed[i]:
                    joint.softStop()
                elif diff > 0:
                    joint.run(1, self._speed[i])
                elif diff < 0:
                    joint.run(0, self._speed[i])

        gripperGoal = self._gripper.toStep(self._target[-1])
        self._gripper.goTo(gripperGoal)
            

    def prepareEngine(self):
        #setup all of the axis for the SlushEngine
        Slush.sBoard()
        joints = [Slush.Motor(0), Slush.Motor(1), Slush.Motor(2), Slush.Motor(3), Slush.Motor(4), Slush.Motor(5)]

        #reset the joints to clear previous errors
        for joint in joints:
            joint.resetDev()
            joint.setMicroSteps(16)

        #some initalization stuff that needs cleanup
        joints[0].setMaxSpeed(self._speed[0])
        joints[1].setMaxSpeed(self._speed[1])
        joints[2].setMaxSpeed(self._speed[2])
        joints[3].setMaxSpeed(self._speed[3])
        joints[4].setMaxSpeed(self._speed[4])
        joints[5].setMaxSpeed(self._speed[5])

        #joint current limits. Still setting manually becuase testing (hold A, run A, acc A, dec, A)
        joints[0].setCurrent(65, 70, 60, 70)
        joints[1].setCurrent(65, 85, 85, 65)
        joints[2].setCurrent(50, 50, 50, 50)
        joints[3].setCurrent(75, 75, 75, 75)
        joints[4].setCurrent(85, 85, 85, 85)
        joints[5].setCurrent(65,65, 65, 65)
        
        self._axis = [
            Axis(-5000,5000,joints[0]),
            Axis(-12500,12500,joints[1]),
            Axis(-22500,22500,joints[2]),
            Axis(-3500,3500,joints[3]),
            Axis(-4000,4000,joints[4]),
            Axis(-1650,1650,joints[5])
        ]
        self._gripper = Gripper()
    
    def _robotMoverThread(robot):
        robot.prepareEngine()
        while not robot.killMover:
            robot.runRobot()
            time.sleep(0.1)
        robot.thread = None

class Gripper:
    def __init__(self):
        #setup the gripper
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.OUT)
        self._pwm = GPIO.PWM(18, 100)
        self._gripper = 7
        self._min = 7
        self._max = 17

    def isBusy(self):
        return False
    
    def getPosition(self):
        return self._gripper

    def goTo(self, nStep):
        if self._gripper == nStep: return
        self._gripper = min(max( nStep, self._min), self._max)
        self._pwm.start(self._gripper)

    def toStep(self, value):
        value = (value + 1) / 2
        value = value * (self._max - self._min)
        return int(value + self._min)
    
