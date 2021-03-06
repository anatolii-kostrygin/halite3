#!/usr/bin/env python3
# Python 3.6

import hlt
from hlt import constants
from hlt.positionals import Direction
import logging


def sign(x):
    if x == 0:
        return 0
    if x > 0:
        return 1
    return -1


""" <<<Game Begin>>> """

# This game object contains the initial game state.
game = hlt.Game()
# At this point "game" variable is populated with initial map data.
# This is a good place to do computationally expensive start-up pre-processing.
# As soon as you call "ready" function below, the 2 second per turn timer will start.
game.ready("MyPythonBot")

# Now that your bot is initialized, save a message to yourself in the log file with some important information.
#   Here, you log here your id, which you can always fetch from the game object by using my_id.
logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))

""" <<<Game Loop>>> """
while True:
    # This loop handles each turn of the game. The game object changes every turn, and you refresh that state by
    #   running update_frame().
    game.update_frame()
    # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    game_map = game.game_map

    # A command queue holds all the commands you will run this turn. You build this list up and submit it at the
    #   end of the turn.
    command_queue = []

    for ship in me.get_ships():
        # go home in turns 101..200, 301..400, etc.
        if (game.turn_number // 100) % 2 == 1:
            if me.shipyard.position.x != ship.position.x:
                command_queue.append(ship.move((sign(me.shipyard.position.x - ship.position.x), 0)))
            elif me.shipyard.position.y != ship.position.y:
                command_queue.append(ship.move((0, sign(me.shipyard.position.y - ship.position.y))))
        else:
            if game_map[ship.position].halite_amount < constants.MAX_HALITE / 10 or ship.is_full:
                direction_towards_best_nearby_choice = max(Direction.get_all_cardinals(),
                               key=lambda card:
                               game_map[ship.position.directional_offset(card)].halite_amount)
                command_queue.append(ship.move(direction_towards_best_nearby_choice))
            else:
                command_queue.append(ship.stay_still())

    # If the game is in the first 200 turns and you have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though - the ships will collide.
    if game.turn_number <= 200 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn())

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)

