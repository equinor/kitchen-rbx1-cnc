import RPi.GPIO as GPIO
import Slush
import threading
import signal
import math
import time
from .Axis import Axis, NullAxis

class Robot:
    def __init__(self):
        
        self._target = [0,0,0,0,0,0]
        self._current = [0,0,0,0,0,0]
        self._axis = []
        # A running thread contineously move robot in small increments to reach the goal target
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
        return {
            'busy': self.isBusy(),
            'targetPos' : self._target,
            'currentPos' : list(map(lambda a: a.getPosition(), self._axis))
        }
  
    def runRobot(self):
        #axis.getPosition() is unreliable. It suddenly spew out big numbers which
        # triggers incremental movement.
        currentPos = []
        for axis in self._axis:
            currentPos.append(axis.getPosition())
        i = 0
        print(currentPos)
        for axis in self._axis:
            if type(axis) is not NullAxis:
                axis.goTo(self._target[i])
            i = i + 1

    def prepareEngine(self):
        #setup all of the axis for the SlushEngine
        Slush.sBoard()
        joints = [Slush.Motor(0), Slush.Motor(1), Slush.Motor(2), Slush.Motor(3), Slush.Motor(4), Slush.Motor(5)]

        #reset the joints to clear previous errors
        for joint in joints:
            joint.resetDev()
            joint.setMicroSteps(16)

        #some initalization stuff that needs cleanup
        joints[0].setMaxSpeed(10)
        joints[1].setMaxSpeed(10)
        joints[2].setMaxSpeed(10)
        joints[3].setMaxSpeed(10)
        joints[4].setMaxSpeed(10)
        joints[5].setMaxSpeed(10)

        #joint current limits. Still setting manually becuase testing (hold A, run A, acc A, dec, A)
        joints[0].setCurrent(65, 85, 75, 70)
        joints[1].setCurrent(65, 85, 85, 65)
        joints[2].setCurrent(50, 50, 50, 50)
        joints[3].setCurrent(75, 75, 75, 75)
        joints[4].setCurrent(85, 85, 85, 85)
        joints[5].setCurrent(65,65, 65, 65)
        
        self._axis = [
            Axis(-5000,5000,joints[0]),
            Axis(-12500,12500,joints[1]),
            Axis(-22500,22500,joints[2]),
            NullAxis(),
            Axis(-4000,4000,joints[4]),
            Axis(-1650,1650,joints[5])
        ]
    
    def _robotMoverThread(robot):
        # TODO: experiment with busy. Can we change position mid change? 
        # Or move non-busy joints independently of other busy joints
        robot.prepareEngine()
        while not robot.killMover:
            if not robot.isBusy():
                robot.runRobot()
        robot.thread = None

class Gripper:
    def __init__(self):
        #setup the gripper
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.OUT)
        self._pwm = GPIO.PWM(18, 100)
        self._gripper = 7

    def isBusy(self):
        return False
    
    def getPosition(self):
        return self._gripper

    def goTo(self, nStep):
        self._gripper = nStep
        self._pwm.start(self._gripper)
