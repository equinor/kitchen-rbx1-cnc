
from inputs import get_gamepad
import RPi.GPIO as GPIO
import Slush
import math
import time


#setup all of the axis for the SlushEngine
b = Slush.sBoard()
joints = [Slush.Motor(0), Slush.Motor(1), Slush.Motor(2), Slush.Motor(3), Slush.Motor(4), Slush.Motor(5)]

#reset the joints to clear previous errors
for joint in joints:
    joint.resetDev()
    joint.setMicroSteps(16)

#some initalization stuff that needs cleanup
joints[0].setMaxSpeed(150)
joints[1].setMaxSpeed(150)
joints[2].setMaxSpeed(250)
joints[3].setMaxSpeed(150)
joints[4].setMaxSpeed(150)
joints[5].setMaxSpeed(150)

#joint current limits. Still setting manually becuase testing (hold A, run A, acc A, dec, A)
joints[0].setCurrent(65, 85, 75, 70)
joints[1].setCurrent(65, 85, 85, 65)
joints[2].setCurrent(50, 50, 50, 50)
joints[3].setCurrent(75, 75, 75, 75)
joints[4].setCurrent(85, 85, 85, 85)
joints[5].setCurrent(65,65, 65, 65)

#setup the gripper
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 100)


def waitForRobot():
    for joint in joints:
        while joint.isBusy(): continue

def robotMove(speed, points):
    
    #wait for the robot to stop doing things
    for joint in joints:
        while joint.isBusy(): continue
            
    #get the current location of the robot
    currentpos = []
    for joint in joints:
        currentpos.append(joint.getPosition())
    
    #make a list of the difference
    differencepose = [points - currentpos for points, currentpos in zip(points, currentpos)]
    maxmove = (max(map(abs, differencepose)))
    i = 0
    for joint in joints:
        try:
            jointspeed = speed * (abs(differencepose[i])/maxmove)
        except:
            jointspeed = 1
        if jointspeed < 1: jointspeed = 1
        joint.setMaxSpeed(math.ceil(jointspeed))
        joint.setMinSpeed(0)
        joint.goTo(int(points[i]))
        i = i + 1


def moveFilePoint(name):
    if name == "LIST":
        with open("example/points.ini") as pointfile:
            for line in pointfile:
                print (line)
    with open("example/points.ini") as pointfile:
        namesfound = 0
        for line in pointfile:
            if line.startswith(name):
                namesfound = 1
                points = line.split(':')
                if points[0] == name:
                    intpoints = []
                    for point in points[1:len(points)]:
                        intpoints.append(int(point))
                    robotMove(80, intpoints)                                
    if not namesfound: print("Point Data not Found")

def runProgram():
    with open("example/run.rbt") as programfile:
        i = 0
        for line in programfile:
            print("N" + str(i) + ":" + line)
            i += 1
            lineinfo = line.rstrip('\n').split(' ')
            if lineinfo[0] == "GOTO":
                moveFilePoint(lineinfo[1])
            if lineinfo[0] == "SLEEP":
                waitForRobot()
                time.sleep(int(lineinfo[1]))
            if lineinfo[0] == "GRIPPER":
                waitForRobot()
                if lineinfo[1] == "OPEN":
                    pwm.start(7)
                if lineinfo[1] == "CLOSE":
                    pwm.start(17)
            if lineinfo[0] == "EXIT":
                break

#start reading the inputs from the gamepad and putting them out the joints
gripper = 7

while 1:
    name = input('Go To Point (no spaced): ')
    moveFilePoint(name)

