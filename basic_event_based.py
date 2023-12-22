import math
import sys
import threading
import warnings
from parameters import meditating_time_distribution, eating_time_distribution


# global variable locks
# one lock for each chopstick
locks = [threading.Lock() for _ in range(5)]

# global variable events
# events list
events = []

# global variable current time
current_time = 0


def add_event(time_until, function):
    events.append(Event(current_time + time_until, function))
    events.sort()


def get_event():
    event = events.pop(0)
    return event.t, event.func


class Event:
    def __init__(self, t, func):
        self.t = t
        self.func = func

    def __gt__(self, other):
        return self.t > other.t

    def __ge__(self, other):
        return self.t >= other.t

    def __lt__(self, other):
        return self.t < other.t

    def __le__(self, other):
        return self.t <= other.t

    def __str__(self):
        return f"{self.t}: {function}"


def visualize_philosophers():
    return "".join([f" {p.state} " for p in philosophers])


class Philosopher:

    def __init__(self, id):
        self.state = "-"
        self.id = id
        self.log = []
        add_event(0, self.meditate)

    def __str__(self):
        return f"Philosopher {id}, State {self.state}"

    def meditate(self):
        self.state = "M"
        self.log.append(f"Meditating,{int(current_time)}\n")
        add_event(meditating_time_distribution(self.id, current_time), self.get_left_chopstick)

    def get_left_chopstick(self):
        self.state = "L"
        self.log.append(f"Left,{int(current_time)}\n")
        # get left chopstick
        if locks[self.id].acquire(blocking=False):
            add_event(0, self.get_right_chopstick)
        else:
            # could not get left chopstick, try again in 1 time unit
            add_event(1, self.get_left_chopstick)

    def get_right_chopstick(self):
        self.state = "R"
        self.log.append(f"Right,{int(current_time)}\n")
        # get right chopstick
        if locks[(self.id + 1) % 5].acquire(blocking=False):
            add_event(0, self.eat)
        else:
            # could not get right chopstick, try again in 1 time unit
            add_event(1, self.get_right_chopstick)

    def eat(self):
        self.state = "E"
        self.log.append(f"Eating,{int(current_time)}\n")
        add_event(eating_time_distribution(), self.return_chopsticks)

    def return_chopsticks(self):
        self.state = "-"
        self.log.append(f"Return,{int(current_time)}\n")

        # return left chopstick
        locks[self.id].release()

        # return right chopsick
        locks[(self.id + 1) % 5].release()

        add_event(0, self.meditate)


if __name__ == "__main__":
    output_to_files_arg = ("-o" in sys.argv or "--output" in sys.argv)
    cnt_max_events_arg = ("-c" in sys.argv or "--count" in sys.argv)

    # parameters
    cnt_max_events = math.inf   # math.inf for simulation until deadlock
    if cnt_max_events_arg:
        arg_idx = list(e == "-c" or e == "--count" for e in sys.argv).index(True)
        if len(sys.argv) < arg_idx or not sys.argv[arg_idx + 1].isdigit():
            warnings.warn("Did not specify parameter count correctly. Defaulting to infinity.", UserWarning)
        else:
            cnt_max_events = int(sys.argv[arg_idx + 1])

    cnt_events_until_deadlock = 100

    # initialize philosophers
    philosophers = [Philosopher(id) for id in range(5)]

    print("simulation starts")
    print("M ... meditating \t L/R ... getting left/right chopstick \t E ... eating \t - ... returning chopstick")
    print(f"Time  :  State of each philosopher")
    cnt_events = 0

    # variables for deadlock detection
    last_state = ""
    cnt_last_state = 0

    # deadlock is detected if nothing changes for cnt_events_until_deadlock events
    while cnt_last_state < cnt_events_until_deadlock and cnt_events < cnt_max_events:
        cnt_events += 1
        current_time, function = get_event()
        # call function corresponding to event
        function()
        # show state
        print(f"{current_time:6.2f}: {visualize_philosophers()}")

        # update variables for deadlock checking
        if visualize_philosophers() == last_state:
            cnt_last_state += 1
        else:
            cnt_last_state = 0
            last_state = visualize_philosophers()

    if cnt_last_state >= cnt_events_until_deadlock:
        print(f"Simulation ended as deadlock is detected after {cnt_events} events. "
              f"In the last {cnt_events_until_deadlock} events nothing changed.")
    else:
        print(f"Simulation ended after {cnt_events} events. No deadlock occurred.")

    if output_to_files_arg:
        for p in philosophers:
            with open(f"philosopher{p.id}.csv", "w") as csvfile:
                csvfile.writelines(p.log)
