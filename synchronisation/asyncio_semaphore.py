import asyncio
from asyncio import Semaphore


async def operation(semaphore: Semaphore):
    print('acquiring semaphore...')
    async with semaphore:
        print('Semaphore acquired!')
        await asyncio.sleep(2)
    print('Semaphore released!')


async def main():
    semaphore = Semaphore(2)  # 2 acquiring allowed, then lock. So only to operation() at the same time
    await asyncio.gather(*[operation(semaphore) for _ in range(4)])

asyncio.run(main())

# in semaphore above you can hack it. If you release more than asquire, the counter will increase more than limit
# bounded semaphore doesn't allow to release more than acquire


async def main():
    semaphore = Semaphore(1)
    print(semaphore._value)

    await semaphore.acquire()
    print(semaphore._value)

    semaphore.release()
    semaphore.release()
    print(semaphore._value)

    await semaphore.acquire()
    await semaphore.acquire()  # it is bad

    print(semaphore._value)

    bounded_semaphore = asyncio.BoundedSemaphore(1)

    await bounded_semaphore.acquire()
    bounded_semaphore.release()
    bounded_semaphore.release()

asyncio.run(main())