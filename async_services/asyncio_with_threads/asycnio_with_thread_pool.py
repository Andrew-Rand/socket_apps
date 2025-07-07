import asyncio
import functools

import requests
from concurrent.futures import ThreadPoolExecutor


def get_status_code(url):
    response = requests.get(url)
    return response.status_code


async def main():
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor(max_workers=100) as pool:  # by default max workers is os.cpu_count() + 4
        urls = ['https://google.com' for i in range(100)]
        tasks = [loop.run_in_executor(pool, functools.partial(get_status_code, url)) for url in urls]
        results = await asyncio.gather(*tasks)
        print(results)


asyncio.run(main())