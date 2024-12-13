import os
import threading
import random
import time

N = 7
Balls = 100000
slots = [0] * N

lock = threading.Lock()
T = os.cpu_count() or 1

def calc_results_with_threads(balls_per_thread, result_slots):
    middle = N // 2

    for _ in range(balls_per_thread):
        k = 0
        for _ in range(N - 1):
            left_or_right = [-1, 1]
            k += random.choice(left_or_right)

        k = middle + k // 2
        k = max(0, min(N - 1, k))
        result_slots[k] += 1

    print(f'Thread ({threading.get_ident()}), slots = {result_slots}')

def calc_results_without_threads():
    slots = [0] * N
    middle = N // 2

    balls = Balls
    while balls > 0:
        k = 0
        for _ in range(N - 1):
            left_or_right = [-1, 1]
            k += random.choice(left_or_right)

        k = middle + k // 2
        k = max(0, min(N - 1, k))
        slots[k] += 1
        balls -= 1

    show_results(slots)

def start_threads():
    threads_list = []
    balls_per_thread = Balls // T

    # Создание временных массивов для каждого потока
    thread_results = [[0] * N for _ in range(T)]

    for i in range(T):
        thread = threading.Thread(target=calc_results_with_threads, args=(balls_per_thread, thread_results[i]))
        threads_list.append(thread)
        thread.start()

    for thread in threads_list:
        thread.join()

    # Сложение результатов из временных массивов в общий массив слотов
    for i in range(T):
        for j in range(N):
            slots[j] += thread_results[i][j]

    show_results(slots)

def show_results(in_slots):
    slots = [(i * 50) // Balls for i in in_slots]

    max_value = max(slots)

    while max_value > 0:
        for slot in slots:
            if slot >= max_value:
                print(" 0 ", end='')
            else:
                print("   ", end='')
        print()
        max_value -= 1

    print(in_slots)
    print(slots)


if __name__ == '__main__':
    start_time_0 = time.perf_counter()
    # calc_results_without_threads()
    end_time_0 = time.perf_counter()

    start_time = time.perf_counter()
    start_threads()
    end_time = time.perf_counter()

    elapsed_time_0 = end_time_0 - start_time_0
    elapsed_time = end_time - start_time
    print(f'Time taken: {elapsed_time_0:.4f} seconds')
    print(f'Time taken with threads: {elapsed_time:.4f} seconds')
