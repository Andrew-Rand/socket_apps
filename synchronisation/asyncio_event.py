import asyncio
from asyncio import Event
import functools


def trigger_event(event: Event) -> None:
    print('Trigerring event')
    event.set()  # set event to True


async def do_work_on_event(event: Event) -> None:
    print('Waiting for event')
    await event.wait()  # waiting for event
    print('Event received! Start working')

    await asyncio.sleep(2)

    print('Finished')

    event.clear()  # set event to False


async def main() -> None:
    event = asyncio.Event()
    asyncio.get_running_loop().call_later(5.0, functools.partial(trigger_event, event))  # set event after 5 seconds
    await asyncio.gather(do_work_on_event(event), do_work_on_event(event))

asyncio.run(main())
