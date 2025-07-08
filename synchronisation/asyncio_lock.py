import asyncio
from asyncio import Lock

async def a(lock: Lock):
    print('Program 1 acquiring lock')
    async with lock:
        # you can use lock.acquire() amd lock.release() but manager is better
        print('Program 1 in lock section')
        await asyncio.sleep(4)
    print('Program 1 released lock')

async def b(lock: Lock):
    print('Program 2 acquiring lock')
    async with lock:
        print('Program 2 in lock section')
        await asyncio.sleep(2)
    print('Program 2 released lock')


async def main():
    lock = Lock()
    await asyncio.gather(a(lock), b(lock))

asyncio.run(main())