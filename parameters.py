from numpy import random

# setting the seed for deterministic runs
# random.seed(1234)

# set strategy by uncommenting one of the following lines:
strategy = "deadlock_possible"
# strategy = "one"
# strategy = "two"

req_chopstick_if_hungrier_than = 0.85


# random time distributions
def meditating_time_distribution(id=None, time=None, hungriness=None):
    if strategy == "deadlock_possible":
        if hungriness is not None:
            if hungriness > req_chopstick_if_hungrier_than:
                return 0
            else:
                return max(random.normal(loc=(-4*hungriness+5), scale=3), 0)
        else:
            return max(random.normal(loc=(5), scale=3), 0)
    elif strategy == "one":
        if time == 0:
            if id == 0:
                return 1
            if id == 4:
                return 3
            if id == 3:
                return 5
            if id == 2:
                return 7
            if id == 1:
                return 9
        return 7
    elif strategy == "two":
        if time == 0:
            if id == 0:
                return 1
            if id == 4:
                return 3
            if id == 3:
                return 5
            if id == 2:
                return 1
            if id == 1:
                return 3
        return 2


def eating_time_distribution():
    if strategy == "deadlock_possible":
        return max(random.normal(loc=3, scale=1), 0)
    elif strategy == "one" or strategy == "two":
        return 1


def cleaning_time_distribution():
    return max(random.normal(loc=1, scale=0.1), 0)


def increase_hungriness(curr_hungriness, time):
    return max(min(curr_hungriness + time * 0.04, 1), 0)


def decrease_hungriness(curr_hungriness, time):
    return max(min(curr_hungriness - time * 0.2, 1), 0)
