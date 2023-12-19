from numpy import random

# setting the seed for deterministic runs
# random.seed(1234)

# set strategy by uncommenting one of the following lines:
# strategy = "deadlock_possible"
strategy = "no_deadlock"


# random time distributions
def meditating_time_distribution(id=None, time=None):
    if strategy == "deadlock_possible":
        return max(random.normal(loc=5, scale=3), 0)
    elif strategy == "no_deadlock":
        if (id + time) % 5 == 0 or (id + time) % 5 == 2:
            return 1
        return 2


def eating_time_distribution():
    if strategy == "deadlock_possible":
        return max(random.normal(loc=3, scale=1), 0)
    elif strategy == "no_deadlock":
        return 1
