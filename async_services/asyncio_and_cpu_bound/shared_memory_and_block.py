import multiprocessing

# one more variant of shared value
# integer_array = multiprocessing.Array('i', [0, 0])


# without blocking, assert not always 10, it is running!
# not always
# comment assert if you want to go

def increment_value(shared_int: multiprocessing.Value):
    shared_int.value += 1

for i in range(100):
    integer = multiprocessing.Value('i', 0)
    processes = [
        multiprocessing.Process(target=increment_value, args=(integer,)),
        multiprocessing.Process(target=increment_value, args=(integer,)),
        multiprocessing.Process(target=increment_value, args=(integer,)),
        multiprocessing.Process(target=increment_value, args=(integer,)),
        multiprocessing.Process(target=increment_value, args=(integer,)),
        multiprocessing.Process(target=increment_value, args=(integer,)),
        multiprocessing.Process(target=increment_value, args=(integer,)),
        multiprocessing.Process(target=increment_value, args=(integer,)),
        multiprocessing.Process(target=increment_value, args=(integer,)),
        multiprocessing.Process(target=increment_value, args=(integer,)),
    ]

    [p.start() for p in processes]
    [p.join() for p in processes]

    print(integer.value)
    assert integer.value == 10



# with blocking
# assert always passes


def increment_value(shared_int: multiprocessing.Value):
    shared_int.get_lock().acquire()  # lock shared variable
    shared_int.value += 1
    shared_int.get_lock().release()  # free shared memory

for i in range(100):
    integer = multiprocessing.Value('i', 0)
    processes = [
        multiprocessing.Process(target=increment_value, args=(integer,)),
        multiprocessing.Process(target=increment_value, args=(integer,)),
        multiprocessing.Process(target=increment_value, args=(integer,)),
        multiprocessing.Process(target=increment_value, args=(integer,)),
        multiprocessing.Process(target=increment_value, args=(integer,)),
        multiprocessing.Process(target=increment_value, args=(integer,)),
        multiprocessing.Process(target=increment_value, args=(integer,)),
        multiprocessing.Process(target=increment_value, args=(integer,)),
        multiprocessing.Process(target=increment_value, args=(integer,)),
        multiprocessing.Process(target=increment_value, args=(integer,)),
    ]

    [p.start() for p in processes]
    [p.join() for p in processes]

    print(integer.value)
    assert integer.value == 10




