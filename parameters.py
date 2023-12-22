from numpy import random

# setting the seed for deterministic runs
# random.seed(1234)

# set strategy by uncommenting one of the following lines:
strategy = "deadlock_possible"
# strategy = "no_deadlock"


# random time distributions
def meditating_time_distribution(id=None, time=None, hungriness=None):
    if strategy == "deadlock_possible":
        if hungriness is not None:
            return max(random.normal(loc=(-4*hungriness+5), scale=3), 0)
        else:
            return max(random.normal(loc=(5), scale=3), 0)
    elif strategy == "no_deadlock":
        if (id + time) % 5 == 0 or (id + time) % 5 == 2:
            return 1
        return 2


def eating_time_distribution():
    if strategy == "deadlock_possible":
        return max(random.normal(loc=3, scale=1), 0)
    elif strategy == "no_deadlock":
        return 1


def cleaning_time_distribution():
    return max(random.normal(loc=1, scale=0.1), 0)


def increase_hungriness(curr_hungriness, time):
    return min(curr_hungriness + time * 0.04, 1)


def decrease_hungriness(curr_hungriness, time):
    return max(curr_hungriness - time * 0.2, 0)
