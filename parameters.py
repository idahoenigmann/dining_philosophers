from numpy import random

# setting the seed for deterministic runs
# random.seed(1234)


# random time distributions
def meditating_time_distribution(id=None, time=None):
    # return max(random.normal(loc=5, scale=3), 0)
    if (id + time) % 5 == 0 or (id + time) % 5 == 2:
        return 1
    return 2


def eating_time_distribution():
    # return max(random.normal(loc=3, scale=1), 0)
    return 1
