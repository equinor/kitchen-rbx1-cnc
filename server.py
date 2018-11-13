from aiohttp import web
import mimetypes
import asyncio

mimetypes.add_type('text/javascript', '.mjs')

serverPos = [0,0,0,0,0,0]
robotPos = [0,0,0,0,0,0]
busy = False

async def getRobot(request):
    return web.json_response(getStatus())

async def postRobot(request):
    global busy, serverPos
    if busy == True :
        return web.HTTPServiceUnavailable

    json = await request.json()
    serverPos = json
    busy = True

    asyncio.create_task(runRobot())
    
    return web.json_response(getStatus())

async def runRobot():
    global busy, serverPos, robotPos
    await asyncio.sleep(1)
    robotPos = serverPos
    busy = False

def getStatus(): 
    global busy, serverPos, robotPos
    return {
        'busy': busy,
        'targetPos' : serverPos,
        'currentPos' : robotPos
    }

app = web.Application()
app.add_routes([web.get('/robot', getRobot),
                web.post('/robot', postRobot)])
app.router.add_static('/', './www', show_index=True)

web.run_app(app)