import multiprocessing
import time

from concurrent.futures import ProcessPoolExecutor


def count(count_to: int) -> int:
    start = time.time()
    counter=0
    while counter < count_to:
        counter += 1
    end = time.time()
    print(f'Count to {count_to}, Total time: {end - start}')
    return counter


if __name__ == '__main__':
    start = time.time()

    cpu_count = multiprocessing.cpu_count()
    print(f'CPU count: {cpu_count}')

    with ProcessPoolExecutor(max_workers=cpu_count) as pool:
        numbers = [1, 3, 200000000, 100000000, 5, 22]
        for result in pool.map(count, numbers):  # iterator, returns results in order. Processes started immediately
            print(result)
    end = time.time()
    print(f'Total time: {end - start}')