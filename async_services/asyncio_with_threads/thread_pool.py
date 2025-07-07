import requests
from concurrent.futures import ThreadPoolExecutor


def get_status_code(url):
    response = requests.get(url)
    return response.status_code


with ThreadPoolExecutor(max_workers=50) as pool:  # by default max workers is os.cpu_count() + 4
    urls = ['https://google.com' for i in range(100)]
    results = pool.map(get_status_code, urls)
    for result in results:
        print(result)