import logging
import threading
import time
from numpy import random

# setting the seed for deterministic runs
# random.seed(1234)

# variables for random time
meditating_time_distribution = lambda: random.normal(loc=5, scale=3)
eating_time_distribution = lambda: random.normal(loc=3, scale=1)

# global variable chopsticks
# 0 means currently not in use
# 1 means currently used by the person on the right
# -1 means currently used by the person on the left
chopsticks = [0, 0, 0, 0, 0]

# global variable locks
# one lock for each chopstick
locks = [threading.Lock() for _ in range(5)]


def philosopher(id):
    while True:
        # meditate
        logging.info(f"Philosopher {id} is meditating.")
        time.sleep(max(meditating_time_distribution(), 0))

        # eat
        logging.info(f"Philosopher {id} is hungry.")
        locks[id].acquire()
        try:
            chopsticks[id] = 1
            logging.info(f"Philosopher {id} got the left chopstick.")

            locks[(id + 1) % 5].acquire()
            try:
                chopsticks[(id + 1) % 5] = -1
                logging.info(f"Philosopher {id} got the right chopstick and started to eat.")
                time.sleep(max(eating_time_distribution(), 0))

                logging.info(f"Philosopher {id} is finished eating.")
            finally:
                pass
        finally:
            chopsticks[id] = 0
            chopsticks[(id + 1) % 5] = 0
            locks[id].release()
            locks[(id + 1) % 5].release()
            logging.info(f"Philosopher {id} returned the chopsticks.")

    logging.info(f"Philosopher {id} died.")


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S")

    philosophers = [threading.Thread(target=philosopher, args=(id,), daemon=True) for id in range(5)]
    for p in philosophers:
        p.start()
    for p in philosophers:
        p.join()
