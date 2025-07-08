import typing

import asyncpg
from asyncpg.pool import Pool
from asyncpg import Record
from aiohttp import web
from aiohttp.web_app import Application
from aiohttp.web_request import Request
from aiohttp.web_response import Response


app = web.Application()
routes = web.RouteTableDef()
DB_KEY = 'database'


async def create_db_pool(app: Application):
    """create connection pool to db and associate it with app"""
    print('Creating db pool')
    pool = await asyncpg.create_pool(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        password='password',
        database='products',
        min_size=6,
        max_size=6,
    )
    app[DB_KEY] = pool


async def clear_db(app: Application):
    """Close connection on app shutdown"""
    app[DB_KEY].close()


@routes.get('/brands')
async def get_brands(request: Request):
    connection = request.app[DB_KEY]  # current app as a property of request
    brand_query = 'SELECT brand_id, brand_name FROM brand'
    results: list[Record] = await connection.fetch(brand_query)
    return web.json_response([dict(brand) for brand in results])


app.on_startup.append(create_db_pool)  # app start hook
app.on_cleanup.append(clear_db)  # app close hood

app.add_routes(routes)

web.run_app(app)