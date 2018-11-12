from aiohttp import web
import mimetypes

mimetypes.add_type('text/javascript', '.mjs')

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

app = web.Application()
app.add_routes([web.get('/api', handle),
                web.get('/api/{name}', handle)])
app.router.add_static('/', './www', show_index=True)

web.run_app(app)