import threading
import time

# N = 10_000_000
N = 80
T = 8
my_lock = threading.Lock()


def func(index):
    pass
    for i in range(index, N, T):
        with my_lock:
            print(index, i)


    # print(f'Hi, from thread {index}')


# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')
    threads_list = []

    for i in range(10):
        thread = threading.Thread(target=func, args=(i,))
        threads_list.append(thread)
        thread.start()

    for i in range(10):
        threads_list[i].join()

    print(f'Hi, from main')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
