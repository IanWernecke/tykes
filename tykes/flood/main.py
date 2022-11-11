import random
from collections import namedtuple
from copy import deepcopy
from functools import lru_cache
from functools import partial
from typing import List
from typing import Tuple

import arcade

from tykes.utils import neighbors

# ?
color_map = dict(
    red=arcade.csscolor.RED,
    orange=arcade.csscolor.ORANGE,
    blue=arcade.csscolor.BLUE,
    green=arcade.csscolor.GREEN,
    purple=arcade.csscolor.PURPLE,
    pink=arcade.csscolor.PINK
)


@lru_cache(maxsize=len(color_map))
def get_color_names() -> List[str]:
    return list(color_map.keys())


def random_color_name() -> str:
    """Select a random color name from the map."""
    return random.choice(get_color_names())


class Flood(arcade.Window):
    """The 'Flood' game displays a box"""

    title = "Flood"

    DONE = False
    SUCCESS = False

    margin_width = 20
    info_height = 60
    info_font_size = 16
    picker_height = 100

    def __init__(self, columns: int = 14, rows: int = 14, box_width: int = 20, box_height: int = 20):

        self.columns = columns
        self.rows = rows

        self.box_height = box_height
        self.box_width = box_width

        self._width = (box_width * columns) + (self.margin_width * 2)
        self._height = (box_height * rows) + (self.margin_width * 2) + self.picker_height + self.info_height

        super().__init__(self._width, self._height, self.title)

        # arcade.set_background_color(arcade.color.AMAZON)
        arcade.set_background_color(arcade.color.WHITE)

        # the "grid" region of the game contains all of the boxes that need to be flooded
        self.grid_bg_sprite = None
        self.grid_width = self.box_width * self.columns
        self.grid_height = self.box_height * self.rows
        self.grid_sprites: arcade.SpriteList
        self.grid_boxes: dict
        self.grid_edge: list

        # the "picker" box shall contain the color buttons to select the flood color
        self.picker_bg_sprite = None
        self.picker_buttons = []
        self.picker_sprites = arcade.SpriteList()
        self.pick_count: int
        self.pick_max = 25
        self.pick_last = None

        self.info_bg_sprite = self.create_sprite(
            x=self.margin_width,
            y=self.margin_width + self.picker_height + self.grid_height,
            width=self.grid_width,
            height=self.info_height,
            color=arcade.csscolor.BLANCHED_ALMOND
        )

        # utility function specific to this object
        self.neighbors = partial(neighbors, max_width=self.columns, max_height=self.rows)

    def setup(self):
        """Initial setup of sprites."""

        # must happen before drawing
        self.clear()

        self.DONE = False
        self.SUCCESS = False

        # define the grid background
        grid_bg_color = random_color_name()
        self.set_grid_background_color(color_name=grid_bg_color)

        # remove any sprites from a previous game
        if hasattr(self, 'grid_sprites'):
            while self.grid_sprites:
                sprite = self.grid_sprites.pop(0)
                sprite.remove_from_sprite_lists()
                sprite.kill()

        self.grid_sprites = arcade.SpriteList()
        self.grid_boxes = dict()
        self.grid_edge = [(0, 0)]

        # define the grid boxes and attach the color name in the process
        for x in range(self.columns):
            for y in range(self.rows):
                if x == 0 and y == 0:
                    self.grid_boxes[(x, y)] = None
                    continue

                color_name = random_color_name()
                sprite = self.create_sprite(
                    self.margin_width + (x * self.box_width),
                    self.margin_width + (y * self.box_height) + self.picker_height,
                    width=self.box_width,
                    height=self.box_height,
                    color=color_name
                )
                sprite.flood_color_name = color_name
                self.grid_sprites.append(sprite)
                self.grid_boxes[(x, y)] = sprite

        self.pick_count = 0

        # define the picker background and buttons
        if self.picker_bg_sprite is None:

            self.picker_bg_sprite = self.create_sprite(
                x=self.margin_width,
                y=self.margin_width,
                width=self.grid_width,
                height=self.picker_height,
                color=arcade.csscolor.BLANCHED_ALMOND
            )

            picker_spacing = int(self.grid_bg_sprite.width / 6)
            for index, name in enumerate(color_map):

                sprite = arcade.SpriteCircle(
                    radius=int(self.picker_height / 4),
                    color=color_map[name]
                )
                sprite.position = (
                    self.margin_width + (picker_spacing * (index + 1)) - int(picker_spacing / 2),
                    self.margin_width + int(self.picker_height / 2)
                )
                sprite.flood_color_name = name
                self.picker_sprites.append(sprite=sprite)

        # ensure the new grid boxes (and grid edge) expands properly and cleans up matching colors
        self.flood(color_name=grid_bg_color)

    def set_grid_background_color(self, color_name: str):
        """Define the grid background sprite for drawing."""

        if self.grid_bg_sprite:
            self.grid_bg_sprite.kill()

        self.grid_bg_sprite = self.create_sprite(
            x=self.margin_width,
            y = self.margin_width + self.picker_height,
            width=(self.grid_width),
            height=self.grid_height,
            color=color_name
        )

        self.pick_last = color_name

    def create_sprite(self, x, y, width, height, color):
        """Create a simple sprite box."""
        if isinstance(color, str):
            color = color_map.get(color, arcade.csscolor.WHITE)
        sprite = arcade.SpriteSolidColor(width=width, height=height, color=color)
        sprite.position = (x + int(width / 2), y + int(height / 2))
        return sprite

    def is_complete(self):
        """Return whether the grid is complete."""
        return not any(self.grid_boxes.values())

    def pick(self, color_name: str) -> int:
        """The player has picked the specified color."""
        if color_name == self.pick_last:
            return self.pick_count

        self.set_grid_background_color(color_name=color_name)
        self.flood(color_name=color_name)

        self.pick_count += 1
        return self.pick_count

    def flood(self, color_name):
        """Redefine the grid edge to wrangle any loose colors."""
        to_process = deepcopy(self.grid_edge)
        while to_process:

            x, y = to_process.pop(0)
            has_neighbor = False
            for nx, ny in self.neighbors(x, y):
                if (neighbor := self.grid_boxes[(nx, ny)]) is None:
                    continue

                has_neighbor = True
                if neighbor.flood_color_name != color_name:
                    continue

                # color match, continue to process
                self.grid_edge.append((nx, ny))
                to_process.append((nx, ny))
                neighbor.remove_from_sprite_lists()
                neighbor.kill()
                self.grid_boxes[(nx, ny)] = None

            if not has_neighbor:
                self.grid_edge.pop(self.grid_edge.index((x, y)))

    #
    #   event handling
    #

    def on_draw(self):
        """Redraw everything (erases existing)"""
        self.clear()

        self.info_bg_sprite.draw()

        # draw any information into the text box
        if self.DONE:
            message = "You won" if self.SUCCESS else "You lost"
            message += f" in {self.pick_count: 2} steps! Press enter to play again."

        else:
            message = f"Score: {self.pick_count: 2} / {self.pick_max:02}"

        arcade.draw_text(
            text=message,
            start_x=self.margin_width + int(self.box_width / 2),
            start_y=self.info_bg_sprite.position[1] - int(self.info_font_size / 2),
            color=arcade.color.BLACK,
            font_size=self.info_font_size,
            bold=True
        )

        self.grid_bg_sprite.draw()
        self.grid_sprites.draw()

        self.picker_bg_sprite.draw()
        self.picker_sprites.draw()

        return super().on_draw()

    def on_key_release(self, key, modifiers):
        """Handle key up events"""
        
        if key == arcade.key.ESCAPE:
            self.close()

        elif key == arcade.key.ENTER and self.DONE:
            self.setup()

        return super().on_key_release(key, modifiers)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):

        # if the user is attempting to pick a new color
        if self.pick_count < self.pick_max:
            if picked := arcade.get_sprites_at_point((x, y), self.picker_sprites):
                self.pick(color_name=picked[0].flood_color_name)
                if self.is_complete():
                    self.DONE, self.SUCCESS = True, True
                elif self.pick_count == self.pick_max:
                    self.DONE = True

        return super().on_mouse_press(x, y, button, modifiers)



def main():

    # window = Flood(width=600, height=400, title="Farkle")
    # window = Flood(columns=2, rows=2, box_height=40, box_width=40)
    window = Flood(box_height=40, box_width=40)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
