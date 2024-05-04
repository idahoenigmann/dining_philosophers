#! /bin/bash

echo "number events, time passed, termination reason"

for ((i = 0; i < 50; i++)); do
	python basic_event_based.py -s $@ | grep "Statistics:" -A1 | grep -v "Statistics:"
done
