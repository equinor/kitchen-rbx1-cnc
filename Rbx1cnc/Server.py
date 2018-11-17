from aiohttp import web, MultipartWriter
import mimetypes
import asyncio
from camera import Camera

class Server():
    def __init__(self, robot):
        mimetypes.add_type('text/javascript', '.mjs')

        self.robot = robot

    async def index(self, request):
        return web.FileResponse('./www/index.html')

    async def getRobot(self, request):
        self.robot.getStatus() 
        return web.json_response(self.robot.getStatus())

    async def postRobot(self, request):
        json = await request.json()
        self.robot.runRobot(json)
        return web.json_response(self.robot.getStatus())
    
    async def cameraFeed(self, request):
            response = web.StreamResponse(status=200, reason='OK', headers={
                'Content-Type': 'multipart/x-mixed-replace; boundary=boundarydonotcross',
            })
            await response.prepare(request)
            camera = Camera()
            while not camera.killCamera:
                data = camera.getFrame()
                if data is None:
                    continue
                await response.write('--{}\r\n'.format('boundarydonotcross').encode('utf-8'))
                await response.write(b'Content-Type: image/jpeg\r\n')
                await response.write('Content-Length: {}\r\n'.format(
                        len(data)).encode('utf-8'))
                await response.write(b"\r\n")
                # Write data
                await response.write(data)
                await response.write(b"\r\n")
                await response.drain()
            return response

    def start(self):
        app = web.Application()
        app.add_routes([web.get('/robot', self.getRobot),
                        web.post('/robot', self.postRobot),
                        web.get('/', self.index),
                        web.get('/camera-feed', self.cameraFeed)])
        app.router.add_static('/', './www', show_index=False)
        web.run_app(app, port=8082)