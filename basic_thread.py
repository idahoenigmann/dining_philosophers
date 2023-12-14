import logging
import threading
import time
from parameters import meditating_time_distribution, eating_time_distribution

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
            logging.info(f"Philosopher {id} got the left chopstick.")

            locks[(id + 1) % 5].acquire()
            try:
                logging.info(f"Philosopher {id} got the right chopstick and started to eat.")
                time.sleep(max(eating_time_distribution(), 0))

                logging.info(f"Philosopher {id} is finished eating.")
            finally:
                pass
        finally:
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
