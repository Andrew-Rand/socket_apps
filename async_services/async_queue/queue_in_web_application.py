import asyncio
from asyncio import Queue, Task
from random import randrange
from aiohttp import web
from aiohttp.web_app import Application
from aiohttp.web_request import Request
from aiohttp.web_response import Response

routes = web.RouteTableDef()
QUEUE_KEY = 'order_queue'
TASKS_KEY = 'order_tasks'


async def process_order_worker(worker_id: int, queue: Queue):
    """Get order from queue and porcess it"""
    while True:
        print(f'Worker {worker_id}: waiting for order...')
        order = await queue.get()  # wait until something in queue
        print(f'Worker {worker_id}: processing order {order}')
        await asyncio.sleep(order)
        print(f'Worker {worker_id}: order {order} processed.')
        queue.task_done()

@routes.post('/order')
async def place_order(request: Request) -> Response:
    """Add order to queue and answer immediately"""
    order_queue = app[QUEUE_KEY]
    await order_queue.put(randrange(5))  # simple example, order is just int
    return Response(body='Order placed!')


async def create_order_queue(app: Application):
    print('Creating order queue and workers...')
    queue: Queue = asyncio.Queue(10)

    app[QUEUE_KEY] = queue
    app[TASKS_KEY] = [asyncio.create_task(process_order_worker(i, queue)) for i in range(5)]

async def destroy_queue(app: Application):
    """Wait 10 seconds and cancel"""
    order_tasks: list[Task] = app[TASKS_KEY]
    queue: Queue = app[QUEUE_KEY]

    print('Waiting for processing orders...')
    try:
        await asyncio.wait_for(queue.join(), timeout=10)
    finally:
        print('Finish, cancel workers')
        [task.cancel() for task in order_tasks]

app = web.Application()
app.on_startup.append(create_order_queue)
app.on_shutdown.append(destroy_queue)
app.add_routes(routes)
web.run_app(app)