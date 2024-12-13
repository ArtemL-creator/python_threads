import os
import threading
import hashlib
import time

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
# alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
N = len(alphabet)
input_pass = "Su5S"
L = len(input_pass)
T = os.cpu_count() or 1  # Выставляем количество потоков в зависимости от железа

stop_event = threading.Event()
found_password = None
lock = threading.Lock()


def get_md5_of_string(input_string):
    return hashlib.md5(input_string.encode()).hexdigest()


def start_threads(in_md5_pass):
    threads_list = []

    for i in range(T):
        thread = threading.Thread(target=brute_force_passwords_with_threads, args=(i, in_md5_pass))
        threads_list.append(thread)
        thread.start()

    for thread in threads_list:
        thread.join()


def brute_force_passwords_with_threads(param, in_md5_pass):
    global found_password
    num = param
    for i in range(num, N ** L, T):
        if stop_event.is_set():
            return
        k = i
        cur_pass = ""
        for j in range(L):
            cur_pass = alphabet[k % N] + cur_pass
            k //= N
        cur_md5 = get_md5_of_string(cur_pass)
        if in_md5_pass == cur_md5:
            with lock:
                if found_password is None:
                    found_password = cur_pass
            stop_event.set()
            return
        print(f'thr {num}, cur_pass {cur_pass}')


def brute_force_passwords_without_threads(in_md5_pass):
    for i in range(N ** L):
        k = i
        cur_pass = ""
        for j in range(L):
            cur_pass = alphabet[k % N] + cur_pass
            k //= N
        cur_md5 = get_md5_of_string(cur_pass)
        if in_md5_pass == cur_md5:
            return cur_pass
        print(f'cur_pass {cur_pass}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    md5_pass = get_md5_of_string(input_pass)
    #
    start_time_0 = time.perf_counter()
    print(brute_force_passwords_without_threads(md5_pass))
    end_time_0 = time.perf_counter()

    start_time = time.perf_counter()
    start_threads(md5_pass)
    end_time = time.perf_counter()

    print(f'Found password is {found_password}')

    elapsed_time_0 = end_time_0 - start_time_0
    elapsed_time = end_time - start_time
    print(f'Time taken: {elapsed_time_0:.4f} seconds')
    print(f'Time taken: {elapsed_time:.4f} seconds')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
