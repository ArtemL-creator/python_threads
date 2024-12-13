import os
import threading
import random
import numpy as np
import time

random.seed()
N = 100000000

T = os.cpu_count() or 1

count_lock = threading.Lock()
total_count = 0


def calc_Pi_with_treads(k):
    global total_count
    count = 0
    for _ in range(N // T):
        x = (random.random() * 2) / T + k - 1
        y = random.random() * 2 - 1
        if x * x + y * y <= 1:
            count += 1

    with count_lock:
        total_count += count
        to = k + 2 / T - 1
        print(f'Thread ({threading.get_ident()}), x E [{k - 1}, {to}], П ~ {(4 * count / N)}')


def calc_Pi_without_treads():
    count = 0
    for _ in range(N):
        x = random.random() * 2 - 1
        y = random.random() * 2 - 1
        if x * x + y * y <= 1:
            count += 1

    print('------------------')
    print(f'П ~ {(4 * count / N)}')
    print('------------------')
    return 4 * count / N


def start_threads():
    threads_list = []
    step = 2 / T
    for k in np.arange(0, 2, step):
        thread = threading.Thread(target=calc_Pi_with_treads, args=(k,))
        threads_list.append(thread)
        thread.start()

    for thread in threads_list:
        thread.join()

    print(f'П ~ {(4 * total_count) / N}')
    print('-------------------')
    return (4 * total_count) / N


if __name__ == '__main__':
    start_time_0 = time.perf_counter()
    # pi_estimate_0 = calc_Pi_without_treads()
    end_time_0 = time.perf_counter()

    start_time = time.perf_counter()
    pi_estimate = start_threads()
    end_time = time.perf_counter()

    elapsed_time_0 = end_time_0 - start_time_0
    elapsed_time = end_time - start_time
    print(f'Time taken: {elapsed_time_0:.4f} seconds')
    print(f'Time taken with threads: {elapsed_time:.4f} seconds')
    # print(f'П ~ {pi_estimate}')
