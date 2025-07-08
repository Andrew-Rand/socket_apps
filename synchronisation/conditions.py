import asyncio
from asyncio import Condition


async def do_work(condition: Condition) -> None:
    while True:
        print('Waiting condition...')
        async with condition:
            print('Lock acquired. Waiting for condition...')
            await condition.wait()
            print('Condition! Lock again and do work')

            await asyncio.sleep(2)

        print('Finished!Lock released completely')


async def fire_event(condition: Condition) -> None:
    while True:
        await asyncio.sleep(5)
        print('Before fire event acquire condition')
        async with condition:
            print('Locked. Notify all workers')
            condition.notify_all()
        print('Notified. Release lock')


async def main():
    condition = Condition()

    asyncio.create_task(fire_event(condition))
    await asyncio.gather(do_work(condition), do_work(condition))


asyncio.run(main())