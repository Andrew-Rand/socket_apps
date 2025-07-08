from datetime import datetime

from aiohttp import web  # module to create web services
from aiohttp.web_request import Request
from aiohttp.web_response import Response


app = web.Application()
routes = web.RouteTableDef()

@routes.get('/time')
async def time(request: Request) -> Response:
    today = datetime.today()
    result = {
        'month': today.month,
        'day': today.day,
        'time': str(today.time()),
    }
    return web.json_response(result)

app.add_routes(routes)

web.run_app(app)