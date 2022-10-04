import random
from copy import deepcopy
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import arcade
import typer

#
#   constants
#

DEFAULT_DICE = list(range(1, 7))
FOUR_OF_A_KIND = True
FIVE_OF_A_KIND = True
SIX_OF_A_KIND = True


BACKGROUND = arcade.color.WHITE


DICE_WIDTH = 50
DICE_HEIGHT = 50
DICE_BORDER_WIDTH = 2
DICE_DOT_RADIUS = 5
DICE_DOT_SPACING = 12


#
#   utility functions
#


@dataclass
class Combination:
    name: str  # triple, straight, three-of-a-kind, four-of-a-kind
    dice: list
    value: int


@dataclass
class ParsedDice:
    combos: List[Combination]
    remainder: List[int]
    value: int


def dice_count(dice: List[int]) -> Dict[int, int]:
    """Count the dice inside of a given list, no zeroes listed."""
    result = dict()
    for die in dice:
        if die not in result:
            result[die] = dice.count(die)
    return result


def dice_contains(super_dice: List[int], sub_dice: List[int]) -> bool:
    """Check whether a superset of dice contains a subset."""
    for side in range(1, 7):
        if sub_dice.count(side) > super_dice.count(side):
            return False
    return True


def parse_dice(dice: List[int]) -> ParsedDice:
    """Parse the combinations, remainder, and value of the given dice."""
    combos = []
    remainder = deepcopy(dice)
    value = 0

    def _check(_name: str, _dice: List[int], _value: int) -> bool:
        """Determine if a combination is present in the given dice."""
        nonlocal combos, remainder, value
        if not dice_contains(remainder, _dice):
            return False
        combos.append(Combination(name=_name, dice=_dice, value=_value))
        for _die in _dice:
            remainder.pop(remainder.index(_die))
        value += _value
        return True

    # straight
    if _check("straight", [1, 2, 3, 4, 5, 6], 1000):
        return ParsedDice(combos=combos, remainder=remainder, value=value)

    # three pairs
    # WARNING: ensure dice given are a deepcopy and reflect the actual remaining
    counted = dice_count(remainder)
    if len(counted.keys()) == 3 and all(counted[side] == 2 for side in counted):
        _check("three_pairs", _dice=deepcopy(remainder), _value=750)

    # oak == one of a kind
    # if any of the counted dice had more than two, the above three pair check
    #   would have failed and this would be possible
    if any(value >= 3 for _, value in counted.items()):

        # six oak
        _check("six_1s", [1] * 6, 1000 * 8)
        for side in range(2, 7):
            _check("six_{side}s", [side] * 6, side * 100 * 8)

        # five oak
        _check("five_1s", [1] * 5, 1000 * 4)
        for side in range(2, 7):
            _check("five_{side}s", [side] * 5, side * 100 * 4)

        # four oak
        _check("four_1s", [1] * 4, 1000 * 2)
        for side in range(2, 7):
            _check("four_{side}s", [side] * 4, side * 100 * 2)

        # three oak
        _check("three_1s", [1] * 3, 1000)
        for side in range(2, 7):
            _check("three_{side}s", [side] * 3, side * 100)

    if not remainder:
        return ParsedDice(combos=combos, remainder=remainder, value=value)

    # ones and fives
    _check("one", [1], 100)
    _check("one", [1], 100)
    _check("five", [5], 50)
    _check("five", [5], 50)

    return ParsedDice(combos=combos, remainder=remainder, value=value)


#
#   drawing functions
#


def draw_d6(center_x, center_y, value, spacing=DICE_DOT_SPACING):
    """Draw a die face at the specified coordinates."""

    # outline
    arcade.draw_rectangle_filled(center_x, center_y, 50, 50, color=BACKGROUND)
    arcade.draw_rectangle_outline(
        center_x=center_x,
        center_y=center_y,
        width=DICE_WIDTH,
        height=DICE_HEIGHT,
        color=arcade.color.BLACK,
        border_width=DICE_BORDER_WIDTH,
    )

    def draw_dot(rel_x, rel_y):
        arcade.draw_circle_filled(
            center_x=center_x + rel_x, center_y=center_y + rel_y, radius=DICE_DOT_RADIUS, color=arcade.color.BLACK
        )

    # center
    if value == 1 or value == 3 or value == 5:
        draw_dot(0, 0)

    # upper right, bottom right
    if value > 1:
        draw_dot(spacing, spacing)
        draw_dot(-spacing, -spacing)

    # bottom right, upper left
    if value > 3:
        draw_dot(spacing, -spacing)
        draw_dot(-spacing, spacing)

    # mid right, mid left
    if value == 6:
        draw_dot(spacing, 0)
        draw_dot(-spacing, 0)


class Farkle(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # arcade.set_background_color(arcade.color.AMAZON)
        arcade.set_background_color(arcade.color.WHITE)

        # get some random dice values
        self.dice_randomize()
        self.dice_locations = [(100 + (index * 60), 100) for index in range(1, 7)]
        print(self.dice_locations)

        # arcade.ShapeElementList

    #
    #   window utilities
    #

    def dice_randomize(self):
        self.dice = sorted(random.randint(1, 6) for _ in range(6))

    def setup(self):

        # must happen before drawing
        self.clear()

        # create a Text object in the future
        arcade.draw_text(text="OK", start_x=20, start_y=20, color=arcade.color.BLACK)
        arcade.draw_rectangle_outline(
            center_x=0, center_y=0, width=50, height=50, color=arcade.color.BLACK, border_width=2
        )

    #
    #   event handling
    #

    def on_update(self, delta_time):

        # arcade.draw_text(text="UP", start_x=20, start_y=20, color=arcade.color.ALICE_BLUE)

        # print('update')

        for index in range(1, 7):
            draw_d6(100 + (index * 60), 100, self.dice[index - 1])

        # SpriteList()
        # dice_hit_list = arcade.check_for_collision_with_list(mouse_location, self.sprite_list)

    def on_key_press(self, key, modifiers):
        """Handle key down events"""

    def on_key_release(self, key, modifiers):
        """Handle key up events"""

        # print(f"key up: {key}, modifiers: {modifiers}")
        if key == arcade.key.ENTER:
            self.dice_randomize()

        elif key == arcade.key.ESCAPE:
            self.close()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        
        print(x, y)


        return super().on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        return super().on_mouse_release(x, y, button, modifiers)


app = typer.Typer()


@app.command(name="farkle")
def main():

    window = Farkle(width=600, height=400, title="Farkle")
    window.setup()
    arcade.run()


if __name__ == "__main__":
    app()
