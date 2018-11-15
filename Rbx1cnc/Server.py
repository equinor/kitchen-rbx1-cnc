from aiohttp import web
import mimetypes
import asyncio

class Server():
    def __init__(self, robot):
        mimetypes.add_type('text/javascript', '.mjs')

        self.robot = robot

    async def getRobot(self, request):
        self.robot.getStatus() 
        return web.json_response(self.robot.getStatus())

    async def postRobot(self, request):
        json = await request.json()
        self.robot.runRobot(json)
        return web.json_response(self.robot.getStatus())

    def start(self):
        app = web.Application()
        app.add_routes([web.get('/robot', self.getRobot),
                        web.post('/robot', self.postRobot)])
        app.router.add_static('/', './www', show_index=True)
        web.run_app(app, port=8082)