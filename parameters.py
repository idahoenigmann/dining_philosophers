from numpy import random

# setting the seed for deterministic runs
random.seed(1234)


# random time distributions
def meditating_time_distribution():
    return random.normal(loc=5, scale=3)


def eating_time_distribution():
    return random.normal(loc=3, scale=1)

