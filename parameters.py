from numpy import random

# setting the seed for deterministic runs
# random.seed(1234)


# random time distributions
def meditating_time_distribution(id=None, time=None):
    return max(random.normal(loc=5, scale=3), 0)


def eating_time_distribution():
    return max(random.normal(loc=3, scale=1), 0)
