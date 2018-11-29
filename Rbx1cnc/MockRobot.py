class MockRobot:
    def __init__(self):
        self._axis = [
            Axis(),
            Axis(),
            Axis(),
            Axis(),
            Axis(),
            Axis()
        ]
        self._target = list(map(lambda a: a.getPosition(), self._axis))
        self._target.append(0) # Mock gripper

    def isBusy(self):
        return False

    def setGoalTarget(self, points):
        self._target = points


    def getStatus(self): 
        pos = list(map(lambda a: a.getPosition(), self._axis))
        pos.append(0)
        return {
            'busy': self.isBusy(),
            'targetPos' : self._target,
            'currentPos' : pos
        }

class Axis():
    def __init__(self):
        self._pos = 0

    def getPosition(self):
        return self._pos