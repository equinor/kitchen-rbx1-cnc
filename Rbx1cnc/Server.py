from aiohttp import web
import mimetypes
import asyncio

class Server():
    def __init__(self):
        mimetypes.add_type('text/javascript', '.mjs')

        self.serverPos = [0,0,0,0,0,0]
        self.robotPos = [0,0,0,0,0,0]
        self.busy = False


    async def getRobot(self, request):
        return web.json_response(self.getStatus())

    async def postRobot(self, request):
        if self.busy == True :
            return web.HTTPServiceUnavailable

        json = await request.json()
        self.serverPos = json
        self.busy = True

        asyncio.create_task(self.runRobot())
        
        return web.json_response(self.getStatus())

    async def runRobot(self):
        await asyncio.sleep(1)
        self.robotPos = self.serverPos
        self.busy = False

    def getStatus(self): 
        return {
            'busy': self.busy,
            'targetPos' : self.serverPos,
            'currentPos' : self.robotPos
        }

    def start(self):
        app = web.Application()
        app.add_routes([web.get('/robot', self.getRobot),
                        web.post('/robot', self.postRobot)])
        app.router.add_static('/', './www', show_index=True)
        web.run_app(app)