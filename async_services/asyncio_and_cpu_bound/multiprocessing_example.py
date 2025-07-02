import time

from multiprocessing import Process


def count(count_to: int) -> int:
    start = time.time()
    counter=0
    while counter < count_to:
        counter += 1
    end = time.time()
    print(f'Count to {count_to}, Total time: {end - start}')
    return counter


start_time = time.time()

process_1 = Process(target=count, args=(100000000,))
process_2 = Process(target=count, args=(200000000,))

process_1.start()  # start process, returns control immediately
process_2.start()

process_1.join()
process_2.join()  # wait until process finishes

# if not use join, main process finishes and kill subprocesses

end_time = time.time()

print(f'Full Time: {end_time - start_time}')


# if you need to get results of subprocesses - use process poll
from multiprocessing import Pool

start_time = time.time()

with Pool() as process_pool:
    process_1 = process_pool.apply_async(count, args=(100000000,))
    process_2 = process_pool.apply_async(count, args=(200000000,))  # both processes started

    # when results is ready, get it and finish processes
    print(process_1.get())
    print(process_2.get())

    end_time = time.time()
    print(f'Full Time: {end_time - start_time}')

