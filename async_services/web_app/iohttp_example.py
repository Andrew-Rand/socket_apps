import asyncio
import aiohttp


async def get_status(session: aiohttp.ClientSession, url: str) -> int:
    timeout = aiohttp.ClientTimeout(total=1) # 1s timeout
    async with session.get(url, timeout=timeout) as response:
        return response.status


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        url = 'https://google.com'
        # example with gather
        # return in order
        # statuses = await asyncio.gather(
        #     *[get_status(session, url) for _ in range(200)], return_exceptions=True
        # )  # gather returns result in order how they provided, exceptions returns in result lists
        # print(statuses)

        # example if need to return which completed first
        # for finished_tasks in asyncio.as_completed([get_status(session, url) for _ in range(200)]):
        #     print(await finished_tasks)  # and ypu can catch exception here

        # example with wait (you can check completed and error tasks)
        tasks = [asyncio.create_task(get_status(session, url)) for _ in range(10)]
        done, pending = await asyncio.wait(tasks, timeout=0.5)

        print(f'Completed tasks: {len(done)}')
        print(f'Pending tasks: {len(pending)}')

        for task in done:
            # you can catch exception here
            status = await task
            print(status)

asyncio.run(main())