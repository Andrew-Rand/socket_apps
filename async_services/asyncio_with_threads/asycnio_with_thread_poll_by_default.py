import asyncio
import functools

import requests
from concurrent.futures import ThreadPoolExecutor


def get_status_code(url):
    response = requests.get(url)
    return response.status_code


async def main():
    urls = ['https://google.com' for i in range(100)]
    tasks = [asyncio.to_thread(get_status_code, url) for url in urls]
    results = await asyncio.gather(*tasks)
    print(results)


asyncio.run(main())