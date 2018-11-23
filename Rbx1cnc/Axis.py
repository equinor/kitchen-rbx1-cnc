import asyncio

class NullAxis():
    def isBusy(self):
        return False
    
    def getPosition(self):
        return 0

    def goTo(self, pos):
        pass

class Axis():
    def __init__(self, min, max, driver):
        self._min = min
        self._max = max
        self._driver = driver

    def isBusy(self):
        return self._driver.isBusy()
    
    def getJoint(self):
        return self._driver

    def getPosition(self):
        return self._fromStep(self._driver.getPosition())

    def goTo(self, pos):
        self._driver.goTo(self._toStep(pos))

    def _toStep(self, value):
        value = (value + 1) / 2
        value = value * (self._max - self._min)
        return int(value + self._min)
    
    def _fromStep(self, value):
        value -= self._min
        value = value / (self._max - self._min)
        return (value * 2) -1


class FakeAxis():
    def __init__(self, loop = True):
        self._pos = 0
        self._target = 0
        if(loop):
            asyncio.create_task(self._updateLoop)

    def isBusy(self):
        return self._pos != self._target
    
    def getPosition(self):
        return self._toStep(self._pos)

    def goTo(self, nStep):
        self._target += nStep

    def _update(self):
        diff = self._pos - self._target
        diff = max( -15, min(15, diff))
        self._pos -= diff

    async def _updateLoop(self):
        while True:
            self._update()
            await asyncio.sleep(0.1)