#!/bin/sh

./halite --no-compression --replay-directory replays/ -vvv --width 32 --height 32 "python3 MyBot.py" "python3 MyBot.py" --seed 42 --turn-limit 1000
