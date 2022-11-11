import random
from typing import Optional, Tuple

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

        self.dice_mats = None

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

        START_X = 100

        MAT_BORDER = 2
        MAT_MARGIN_INNER = 1
        MAT_MARGIN_OUTER = 1
        MAT_SEP = 10
        MIDDLE_Y = 30
        MAT_WIDTH = DICE_WIDTH + (MAT_BORDER * 2) + (MAT_MARGIN_INNER * 2) + (MAT_MARGIN_OUTER * 2)
        MAT_HEIGHT = DICE_HEIGHT + (MAT_BORDER * 2) + (MAT_MARGIN_INNER * 2) + (MAT_MARGIN_OUTER * 2)

        # create the dice mats for rendering clicks/selection
        self.dice_mats = arcade.SpriteList()

        for index in range(7):
            mat = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            mat.position = START_X + (index * (MAT_WIDTH + MAT_SEP)), MIDDLE_Y
            self.dice_mats.append(mat)

        # create a Text object in the future
        arcade.draw_text(text="OK", start_x=20, start_y=20, color=arcade.color.BLACK)
        arcade.draw_rectangle_outline(
            center_x=0, center_y=0, width=50, height=50, color=arcade.color.BLACK, border_width=2
        )

    #
    #   event handling
    #

    def on_draw(self):
        """Redraw everything (erases existing)"""
        self.clear()

        self.dice_mats.draw()

        return super().on_draw()

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

        # Get list of cards we've clicked on
        # cards = arcade.get_sprites_at_point((x, y), self.card_list)

        # note: this works!
        mats = arcade.get_sprites_at_point((x, y), self.dice_mats)
        if mats:
            print(mats)

        return super().on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        return super().on_mouse_release(x, y, button, modifiers)


# app = typer.Typer(no_args_is_help=False)
# app = typer.Typer()


# @app.command(name="farkle")
def main():

    window = Farkle(width=600, height=400, title="Farkle")
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
