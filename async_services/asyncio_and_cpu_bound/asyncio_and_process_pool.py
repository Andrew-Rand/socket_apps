import asyncio
import multiprocessing
import time

from concurrent.futures import ProcessPoolExecutor
from functools import partial


def count(count_to: int) -> int:
    start = time.time()
    counter=0
    while counter < count_to:
        counter += 1
    end = time.time()
    print(f'Count to {count_to}, Total time: {end - start}')
    return counter


async def main():
    with ProcessPoolExecutor() as process_pool:
        loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
        nums = [1, 3, 200000000, 100000000, 5, 22]
        calls: list[partial[int]] = [partial(count, num) for num in nums]  # use partial to add arguments in functions

        processes = []
        for call in calls:
            processes.append(loop.run_in_executor(process_pool, call))  # asyncio + processes

        # results = await asyncio.gather(*processes) # wait for processes, results in order
        # for result in results:
        #     print(result)

        for finished_process in asyncio.as_completed(processes):  # result when it is ready
            print(await finished_process)


asyncio.run(main())