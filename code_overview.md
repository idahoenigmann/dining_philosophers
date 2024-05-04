Implementation details

Main loop:
```
while no deadlock detected:
    show state of philsophers
    get next event
    call function corresponding to event
```

Example function:
```
def meditate():
    set state to meditating
    get time needed for this instance of meditation
    add event 'get left chopstick' in time specified above
```

Making sure a chopstick is not used simultaneously by use of locks.