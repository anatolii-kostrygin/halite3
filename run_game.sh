#!/bin/sh

./halite --no-compression --replay-directory replays/ -vvv --width 32 --height 32 --seed 42 --turn-limit 1000 "python3 GreedyBot1.py" "python3 DefaultBot.py" --override-names "GreedyBot1" --override-names "DefaultBot"
