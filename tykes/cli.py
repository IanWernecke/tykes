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
from tykes.maze import run as run_maze

#
#   globals
#

app = typer.Typer()


# pygame must be initialized before any fonts are declared or anything
# pygame.init()


@app.command(name="maze")
def maze_cmd(width: int = 20, height: int = 20):
    """Generate a maze for the tike."""
    sys.exit(run_maze(width=width, height=height))


@app.command("memory")
def memory_cmd():
    """Placeholder command for the next game planned."""


@app.command("test")
def test_cmd():
    """A place to test new things before they are deployed."""
    pygame.init()

    # set the initial window size, fill, display, and wait
    window = pygame.display.set_mode((640, 480))
    window.fill(color.white)

    pygame.display.flip()
    time.sleep(5)

    # set the updated window size, fill, display, and wait
    window = pygame.display.set_mode((900, 600))
    window.fill(color.white)

    pygame.display.flip()
    time.sleep(5)


if __name__ == "__main__":
    app()
