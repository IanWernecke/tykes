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

# from tykes.farkle.main import app as farkle_app
from tykes.farkle.main import main as farkle_main
from tykes.flood.main import main as flood_main
from tykes.maze import main as maze_main
from tykes.memory import main as memory_main

#
#   globals
#

app = typer.Typer(no_args_is_help=True)


@app.command(name="farkle")
def farkle_cmd():
    """Play the dice-rolling game farkle."""
    sys.exit(farkle_main())


@app.command(name="flood")
def flood_cmd():
    """Play the simple color game 'Flood'."""
    sys.exit(flood_main())


@app.command(name="maze")
def maze_cmd(width: int = 20, height: int = 20):
    """Generate a maze for the tike."""
    sys.exit(maze_main(width=width, height=height))


@app.command("memory")
def memory_cmd(width: int = 6, height: int = 4):
    """Placeholder command for the next game planned."""
    sys.exit(memory_main(width=width, height=height))


@app.command("test")
def test_cmd():
    """A place to test new things before they are deployed."""
    pygame.init()

    font = pygame.font.SysFont(None, size=20)

    # set the initial window size, fill, display, and wait
    window = pygame.display.set_mode((640, 480))
    window.fill(color.white)

    # unknown_surface = font.render("?", True, color.black)
    # unknown_rect = unknown_surface.get_rect()
    # window.blit(
    #     font.render(b"\x01\x02".decode(), True, color.black),
    #     dest=(30, 30)
    # )
    window.blit(font.render("".join(chr(index + 1) for index in range(64)), True, color.black), dest=(30, 30))

    # window.blit(unknown_surface, dest=(30, 30))

    pygame.display.flip()
    time.sleep(5)

    # # set the updated window size, fill, display, and wait
    # window = pygame.display.set_mode((900, 600))
    # window.fill(color.white)

    # pygame.display.flip()
    # time.sleep(5)


if __name__ == "__main__":
    app()
