import os
import threading
import time
import random


class Chopstick:
    def __init__(self):
        self.lock = threading.Lock()


class Philosopher(threading.Thread):
    def __init__(self, number, left_chopstick, right_chopstick):
        super().__init__()
        self.number = number
        self.left_chopstick = left_chopstick
        self.right_chopstick = right_chopstick

    def eat(self):
        # Имитация времени на еду
        time.sleep(random.uniform(0.5, 1))

    def think(self):
        # Имитация времени на размышления
        time.sleep(random.uniform(0.1, 0.5))

    def run(self):
        while True:
            print(f"{self.number} is thinking.")
            self.think()

            print(f"{self.number} is hungry.")
            # Упорядоченный захват палочек для предотвращения взаимной блокировки
            if self.number % 2 == 0:
                first, second = self.left_chopstick, self.right_chopstick
            else:
                first, second = self.right_chopstick, self.left_chopstick

            with first.lock:  # Захватываем левую палочку
                print(f"{self.number} picked up left chopstick.")
                with second.lock:  # Захватываем правую палочку
                    print(f"{self.number} picked up right chopstick.")
                    self.eat()
                    print(f"{self.number} finished eating and put down chopsticks.")


if __name__ == "__main__":
    num_philosophers = os.cpu_count() or 1
    chopsticks = [Chopstick() for _ in range(num_philosophers)]
    philosophers = []

    for i in range(num_philosophers):
        left_chopstick = chopsticks[i]
        right_chopstick = chopsticks[(i + 1) % num_philosophers]
        philosopher = Philosopher(i, left_chopstick, right_chopstick)
        philosophers.append(philosopher)
        philosopher.start()

    # Ожидание завершения всех потоков (в данном случае они бесконечные)
    for philosopher in philosophers:
        philosopher.join()
