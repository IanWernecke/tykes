"""This file contains the primary cli entry point for the project."""

#  _         _
# | |_ _   _| | _____  ___
# | __| | | | |/ / _ \/ __|
# | |_| |_| |   <  __/\__ \
#  \__|\__, |_|\_\___||___/
#      |___/


import random
import sys
import time
from copy import deepcopy
from typing import Tuple

import pygame
import typer
from loguru import logger

# module imports
from tykes import color
from tykes.maze import Maze
from tykes.utils import frame_rate

#
#   globals
#

app = typer.Typer()


# pygame must be initialized before any fonts are declared or anything
pygame.init()

# this variable is used to hold the primary pygame window, when initialized
# it is not initialized here because we want --help to not spawn a window
window = None


@app.command(name="maze")
def maze_cmd(width: int = 20, height: int = 20):
    """Generate a maze for the tike."""

    # create the maze object and render it onto the window
    maze = Maze(width=width, height=height)

    # define the primary window size now that the maze's width and height have been defined
    # match the maze width, maze height + information
    window = pygame.display.set_mode((maze.px_width, maze.px_height + maze.score_surface.get_height()))
    window.fill(color.white)

    # draw the maze onto the window
    maze.draw(window)
    pygame.display.flip()

    # define the movement keys
    movement_keys = {pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1), pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0)}

    # enter the event loop
    # 4643 frames drawn prior to frame rate implementation
    for _ in frame_rate(frames_per_second=60):

        # for each of the events in the queue, obtain it
        for event in pygame.event.get():

            # if the window 'close' event occurs
            if event.type == pygame.QUIT:
                sys.exit()

            # key has been pressed
            if event.type == pygame.KEYDOWN:

                # escape key pressed
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

                # backspace, move back on the trail
                if event.key == pygame.K_BACKSPACE:
                    if not maze.move_back():
                        logger.warning("Failed to move backwards.")

                # if an arrow key has been pressed, try to move
                if event.key in movement_keys:

                    # try to move to an adjacent point
                    point_mod = movement_keys[event.key]
                    point = maze.point[0] + point_mod[0], maze.point[1] + point_mod[1]
                    maze.move(point)

        # draw the maze onto the window
        maze.draw(window)
        pygame.display.flip()

        # exit if the game is won
        if maze.complete:
            time.sleep(5)
            maze.generate()


@app.command("memory")
def memory_cmd():
    """Placeholder command for the next game planned."""


if __name__ == "__main__":
    app()
