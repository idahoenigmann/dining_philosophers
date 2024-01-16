import math
import sys
import threading
import warnings
import itertools
from parameters import *


# global variable locks
# one lock for each chopstick
locks = [threading.Lock() for _ in range(5)]

# global variable events
# events list
events = []

# global variable current time
current_time = 0


def add_event(time_until, event_function):
    e = Event(current_time + time_until, event_function)
    events.append(e)
    events.sort()
    return e


def remove_event(event):
    events.remove(event)


def get_event():
    event = events.pop(0)
    return event.t, event.func


class Event:
    id_iter = itertools.count()

    def __init__(self, t, func):
        self.t = t
        self.func = func
        self.event_id = next(Event.id_iter)

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

    def __eq__(self, other):
        return self.event_id == other.event_id


def visualize_states():
    return "".join([f" {philosopher.state} " for philosopher in philosophers])


def visualize_hungriness():
    return "".join([f" {philosopher.hungriness:2.1f} " for philosopher in philosophers])


class Philosopher:

    def __init__(self, philosopher_id, hungriness, cleaning, communicate):
        self.state = "-"
        self.id = philosopher_id
        self.log = []
        if hungriness:
            self.hungriness = 0.0
            self.last_hungriness = [0.0, 0]  # current_hungriness, current_time
        else:
            self.hungriness = None
        self.cleaning = cleaning
        self.communicate = communicate
        self.next_event = None
        self.meditate()

    def __str__(self):
        if self.hungriness is None:
            return f"Philosopher {self.id}, State {self.state}"
        else:
            return f"Philosopher {self.id}, State {self.state}, Hungriness {self.hungriness}"

    def meditate(self):
        # set state to meditating
        self.state = "M"
        # append state change to log used for visualization
        self.log.append(f"Meditating,{int(current_time)}\n")

        # get time needed for meditation
        meditating_time = meditating_time_distribution(self.id, current_time, self.hungriness)

        if self.hungriness is not None:
            # remember old hungriness in case this event is interrupted
            self.last_hungriness = [self.hungriness, current_time]
            # increase hungriness for time spend in meditation
            self.hungriness = increase_hungriness(self.hungriness, meditating_time)
        # get left chopstick after finished with meditation
        self.next_event = add_event(meditating_time, self.get_left_chopstick)

    def get_left_chopstick(self):
        # set state to left chopstick
        self.state = "L"
        # append state change to log used for visualization
        self.log.append(f"Left,{int(current_time)}\n")

        # try to get left chopstick
        if locks[self.id].acquire(blocking=False):
            # successful, now add get right chopstick as next event
            self.next_event = add_event(0, self.get_right_chopstick)
        else:
            # could not get left chopstick, try again in 1 time unit
            self.next_event = add_event(1, self.get_left_chopstick)

            if self.hungriness is not None:
                # remember old hungriness in case this event is interrupted
                self.last_hungriness = [self.hungriness, current_time]
                # increase hungriness for time spend waiting
                self.hungriness = increase_hungriness(self.hungriness, 1)

                if self.communicate and self.hungriness > req_chopstick_if_hungrier_than:
                    print(f"{self.id} requested chopstick from {(self.id - 1) % 5}")
                    # request chopstick from left philosopher
                    philosophers[(self.id - 1) % 5].req_chopstick()

    def get_right_chopstick(self):
        self.state = "R"
        self.log.append(f"Right,{int(current_time)}\n")

        # get right chopstick
        if locks[(self.id + 1) % 5].acquire(blocking=False):
            self.next_event = add_event(0, self.eat)
        else:
            # could not get right chopstick, try again in 1 time unit
            self.next_event = add_event(1, self.get_right_chopstick)
            if self.hungriness is not None:
                self.last_hungriness = [self.hungriness, current_time]
                self.hungriness = increase_hungriness(self.hungriness, 1)
                if self.communicate and self.hungriness > req_chopstick_if_hungrier_than:
                    print(f"{self.id} requested chopstick from {(self.id + 1) % 5}")
                    philosophers[(self.id + 1) % 5].req_chopstick()

    def eat(self):
        self.state = "E"
        self.log.append(f"Eating,{int(current_time)}\n")

        eating_time = eating_time_distribution()

        if self.hungriness is not None:
            self.last_hungriness = [self.hungriness, current_time]
            self.hungriness = decrease_hungriness(self.hungriness, eating_time)
        if self.cleaning:
            self.next_event = add_event(eating_time, self.clean)
        else:
            self.next_event = add_event(eating_time, self.return_chopsticks)

    def clean(self):
        self.state = "C"
        self.log.append(f"Cleaning,{int(current_time)}\n")

        cleaning_time = cleaning_time_distribution()
        if self.hungriness is not None:
            self.last_hungriness = [self.hungriness, current_time]
            self.hungriness = increase_hungriness(self.hungriness, cleaning_time)
        self.next_event = add_event(cleaning_time, self.return_chopsticks)

    def return_chopsticks(self):
        # set state to returning chposticks
        self.state = "-"
        # append state change to log used for visualization
        self.log.append(f"Return,{int(current_time)}\n")

        # return left chopstick, if currently held
        if locks[self.id].locked():
            locks[self.id].release()

        # return right chopstick, if currently held
        if locks[(self.id + 1) % 5].locked():
            locks[(self.id + 1) % 5].release()

        # schedule meditate as next event
        self.next_event = add_event(0, self.meditate)


    def req_chopstick(self):
        # if hungry or already cleaning don't give up chopstick
        if decrease_hungriness(self.last_hungriness[0], (current_time - self.last_hungriness[1])) > req_chopstick_if_hungrier_than:
            print(f"request denied: too hungry")
            return
        elif self.state == "C" or self.state == "-":
            print(f"request denied: already cleaning or returning")
            return

        print(f"request accepted")

        # reschedule my next event
        remove_event(self.next_event)

        if self.state == "R":
            # give up chopsticks
            self.return_chopsticks()
        elif self.state == "E":
            # update hungriness
            self.hungriness = decrease_hungriness(self.last_hungriness[0], (current_time - self.last_hungriness[1]))

            if self.cleaning:
                self.clean()
            else:
                self.return_chopsticks()


if __name__ == "__main__":
    if "-h" in sys.argv or "--help" in sys.argv:
        print(f"Usage: {sys.argv[0]} [OPTION]...\nEvent based simulation of dining philosophers problem.\n"
              f"Example: {sys.argv[0]} -o -c 500\n\n"
              f"Options:\n"
              f"  -h, --help         print this help message\n"
              f"  -c, --count <NUM>  stop simulation after at most NUM events\n"
              f"  -o, --output       generate output csv-files used for visualization\n"
              f"  --hungry           enable hungriness and starvation\n"
              f"  --clean            enable cleaning of chopsticks after use\n"
              f"  --communicate      enable communication with neighboring philosophers")
        exit()

    output_to_files_arg = ("-o" in sys.argv or "--output" in sys.argv)
    cnt_max_events_arg = ("-c" in sys.argv or "--count" in sys.argv)
    hungriness_arg = ("--hungry" in sys.argv)
    cleaning_arg = ("--clean" in sys.argv)
    communicate_arg = ("--communicate" in sys.argv)

    if communicate_arg and not hungriness_arg:
        warnings.warn("Did not specify hungry option, but did specify communicate. Adding hungry option.")
        hungriness_arg = True

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
    philosophers = [Philosopher(philosopher_id, hungriness_arg, cleaning_arg, communicate_arg) for philosopher_id in range(5)]

    if cleaning_arg:
        print("M ... meditating \t L/R ... getting left/right chopstick \t E ... eating \t C ... cleaning"
              " \t - ... returning chopstick")
    else:
        print("M ... meditating \t L/R ... getting left/right chopstick \t E ... eating \t - ... returning chopstick")
    if hungriness_arg:
        print(f"Time  :  State                Hungriness")
    else:
        print(f"Time  :  State")
    cnt_events = 0

    # variables for deadlock detection
    last_state = ""
    cnt_last_state = 0

    # deadlock is detected if nothing changes for cnt_events_until_deadlock events
    while cnt_last_state < cnt_events_until_deadlock and cnt_events < cnt_max_events:
        # show state
        if hungriness_arg:
            print(f"{current_time:6.2f}: {visualize_states()} \t {visualize_hungriness()}")
        else:
            print(f"{current_time:6.2f}: {visualize_states()}")

        cnt_events += 1
        current_time, function = get_event()
        # call function corresponding to event
        function()

        # check if a philosopher died
        if hungriness_arg:
            someone_died = False
            for p in philosophers:
                if p.hungriness == 1:
                    print(f"Philosopher {p.id} died from starvation.")
                    someone_died = True
            if someone_died:
                break

        # update variables for deadlock checking
        if visualize_states() == last_state:
            cnt_last_state += 1
        else:
            cnt_last_state = 0
            last_state = visualize_states()

    if cnt_last_state >= cnt_events_until_deadlock:
        print(f"Simulation ended as deadlock is detected after {cnt_events} events. "
              f"In the last {cnt_events_until_deadlock} events nothing changed.")
    elif cnt_events >= cnt_max_events:
        print(f"Simulation ended after {cnt_events} events. No deadlock occurred.")
    else:
        print(f"Simulation ended after a philosopher died after {cnt_events} events.")

    if output_to_files_arg:
        for p in philosophers:
            with open(f"philosopher{p.id}.csv", "w") as csvfile:
                csvfile.writelines(p.log)
