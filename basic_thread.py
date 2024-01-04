import logging
import threading
import time
from parameters import meditating_time_distribution, eating_time_distribution

# global variable locks
# one lock for each chopstick
locks = [threading.Lock() for _ in range(5)]


def philosopher(philosopher_id):
    while True:
        # meditate
        logging.info(f"Philosopher {philosopher_id} is meditating.")
        time.sleep(meditating_time_distribution())

        # eat
        logging.info(f"Philosopher {philosopher_id} is hungry.")
        locks[philosopher_id].acquire()
        try:
            logging.info(f"Philosopher {philosopher_id} got the left chopstick.")

            locks[(philosopher_id + 1) % 5].acquire()
            try:
                logging.info(f"Philosopher {philosopher_id} got the right chopstick and started to eat.")
                time.sleep(eating_time_distribution())

                logging.info(f"Philosopher {philosopher_id} is finished eating.")
            finally:
                pass
        finally:
            locks[philosopher_id].release()
            locks[(philosopher_id + 1) % 5].release()
            logging.info(f"Philosopher {philosopher_id} returned the chopsticks.")


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S")

    philosophers = [threading.Thread(target=philosopher, args=(p_id,), daemon=True) for p_id in range(5)]
    for p in philosophers:
        p.start()
    for p in philosophers:
        p.join()
