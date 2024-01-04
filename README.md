# Dining Philosophers

Python implementation for Modelling and Simulation project

### Implementations:
* thread based (only minimal version)
* event based

### Features:
* basic version
* visualization
* hungriness
* cleaning
* communication with neighboring philosophers

### Installation
Make sure you installed numpy and matplotlib packages.

Then get the code and run it.
```shell
git clone https://github.com/idahoenigmann/dining_philosophers
cd dining_philosophers
```

```shell
python basic_event_based.py -o -c 500
python philosopher_visual.py
```

You should see a visualization of the five philosophers meditating
and eating.

Try changing some of the parameters by setting them in [parameters.py](parameters.py).
A few different time distributions are already available and can be specified with the
parameter ```strategy```.

To enable the features hungriness, cleaning and communication have a look at one of the following
usages:
```shell
python basic_event_based.py --help
python basic_event_based --hungry --clean --communicate
```