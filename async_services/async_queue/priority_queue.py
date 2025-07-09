import asyncio
from asyncio import Queue, PriorityQueue


async def worker(queue: Queue):
    while not queue.empty():
        work_item: tuple[int, str] = queue.get_nowait()
        print(f'Working on item {work_item}')
        queue.task_done()


async def main():
    priority_queue = PriorityQueue()
    work_items = [
        (3, 'Lowest priority'),
        (1, 'High priority'),
        (2, 'Mdium priority'),
    ]

    worker_task = asyncio.create_task(worker(priority_queue))

    for work in work_items:
        # add elements to queue
        priority_queue.put_nowait(work)

    await asyncio.gather(priority_queue.join(), worker_task)

asyncio.run(main())