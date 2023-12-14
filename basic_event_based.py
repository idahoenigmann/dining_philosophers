import threading
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
        add_event(0, self.meditate)

    def __str__(self):
        return f"Philosopher {id}, State {self.state}"

    def meditate(self):
        self.state = "M"
        add_event(meditating_time_distribution(), self.get_left_chopstick)

    def get_left_chopstick(self):
        self.state = "L"
        # get left chopstick
        if locks[self.id].acquire(blocking=False):
            add_event(0, self.get_right_chopstick)
        else:
            # could not get left chopstick, try again in 1 time unit
            add_event(1, self.get_left_chopstick)

    def get_right_chopstick(self):
        self.state = "R"
        # get right chopstick
        if locks[(self.id + 1) % 5].acquire(blocking=False):
            add_event(0, self.eat)
        else:
            # could not get right chopstick, try again in 1 time unit
            add_event(1, self.get_right_chopstick)

    def eat(self):
        self.state = "E"
        add_event(eating_time_distribution(), self.return_chopsticks)

    def return_chopsticks(self):
        self.state = "-"

        # return left chopstick
        locks[self.id].release()

        # return right chopsick
        locks[(self.id + 1) % 5].release()

        add_event(0, self.meditate)


if __name__ == "__main__":
    # initialize philosophers
    philosophers = [Philosopher(id) for id in range(5)]

    print("simulation starts")
    cnt_events = 0

    # variables for deadlock detection
    last_state = ""
    cnt_last_state = 0

    # deadlock is detected if nothing changes for 100 events
    while cnt_last_state < 100 and cnt_events < 300:
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

    print("deadlock detected, ended simulation")
