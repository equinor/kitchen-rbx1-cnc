import asyncio

class FakeAxis():
    def __init__(self, loop = True):
        self._pos = 0
        self._target = 0
        if(loop):
            asyncio.create_task(self._updateLoop)

    def isBusy(self):
        return self._pos != self._target
    
    def getPosition(self):
        return self._pos

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

    