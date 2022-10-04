# standard imports
import sys
import time
from collections import OrderedDict

# installed imports
import pygame

# module imports
from tykes import color
from tykes.utils import create_text_box

pygame.init()


class Positions:

    UPPER_LEFT = 0
    UPPER_CENTER = 1
    UPPER_RIGHT = 2

    MIDDLE_LEFT = 3
    MIDDLE_CENTER = 4
    MIDDLE_RIGHT = 5

    BOTTOM_LEFT = 6
    BOTTOM_CENTER = 7
    BOTTOM_RIGHT = 8


# TODO: might be worth thinking about
# class Layer(pygame.Surface):

#     def __init__(self, name, position):
#         self.name = name
#         self.position = position

#     def draw(self, window):
#         window.blit(self.surface, dest=self.position)


class Game:
    """Handles and controls the primary game window."""

    def __init__(
        self,
        title: str = "Game",
        dimensions: tuple = (640, 480),
        background: tuple = color.white,
        frame_rate: int = 120,
    ):
        """Initialize the primary window and set up the values to be used during rendering."""

        # TODO: perhaps pygame.init() here?

        self.window = pygame.display.set_mode(dimensions)
        self.window.set_colorkey(color.transparent)
        pygame.display.set_caption(title)

        # store values on self to be used later
        self.dimensions = dimensions
        self.width, self.height = dimensions
        self.background = background
        self._drawing = True
        self._events_called = True

        # calculate the interval between draws
        self.frame_rate = frame_rate
        if self.frame_rate is not None:
            self.frame_interval = 1.0 / frame_rate
        else:
            self.frame_interval = None
        self.last_draw = 0

        # the layers need to be set an ordered array that can be accessed by key and drawn one at time onto the window before rendering
        # note: this could be done via list but I think accessing them arbitrarily is a great idea for later updating
        # note: an ordered dict can be iterated with .items() as a normal dict, and in order
        self.layers = OrderedDict()
        self.positions = OrderedDict()

    def add_layer(self, name, position=None, dimensions=None, surface=None, background=color.transparent):
        """Add a layer to be drawn onto the window during every call to 'draw'."""

        # if the location was not given, add it to the upper left
        if position is None:
            position = (0, 0)

        # if a surface was not given
        if surface is None:

            # if dimensions were not given, use the dimensions of the window
            if dimensions is None:
                dimensions = self.dimensions

            # create the surface to be drawn on
            # note: should this be filled with transparent?
            surface = pygame.Surface(dimensions)
            surface.set_colorkey(color.transparent)
            surface.fill(color=background)

        # store the location where the surface is to be drawn
        self.positions[name] = position

        # store the surface in the ordered dictionary
        self.layers[name] = surface

    def draw(self):
        """Fill the window with the background color, draw each layer, then flip the display."""

        # fill the window the with background color
        self.window.fill(self.background)

        # draw each of the layers in order
        for name, layer in self.layers.items():
            self.window.blit(layer, dest=self.positions.get(name, (0, 0)))

        # flip the window to display the drawn layers
        pygame.display.flip()

    def events(self):
        """Iterate each of the events given to pygame, but exit upon conditions."""
        self._events_called = True

        # for each of the events in the queue, obtain it
        for event in pygame.event.get():

            # if the window 'close' event occurs
            if event.type == pygame.QUIT:
                self._drawing = False

            # key has been pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._drawing = False

            yield event

    def move(self, layer, position):
        """Move a layer's position to be drawn to somewhere else."""
        # ensure the layer exists
        if layer not in self.layers:
            raise ValueError(f'Layer not found: "{layer}"')

        # if an exact point is given
        if isinstance(position, tuple):
            self.positions[layer] = position
            return True

        # use relative points to move the layer around
        # relative positions ex: TOP_LEFT, BOTTOM_RIGHT
        # if getattr(Positions, position)

    @property
    def drawing(self, frame_rate: int = 120):
        """
        This property is accessed for each loop.
        It should determine whether the game should continue to be played.
        It should be responsible for drawing the game onto the window.
        """
        self.draw()
        if not self._events_called:
            return False

        # sleep until the interval has passed
        if self.frame_interval is not None:
            next_draw = self.last_draw + self.frame_interval
            now = time.time()
            if now < next_draw:
                time.sleep(next_draw - now)
            self.last_draw = next_draw

        self._events_called = False
        return self._drawing


class Memory(Game):

    # define the spaces around the outside and between the cards
    card_margin = 10
    card_sep = 10

    # card width and height include card borders (both sides, each way)
    card_border = 2
    card_width = 30
    card_height = 40

    # define variables for the selection
    selection_border_width = 2
    selection_border_radius = 2

    # define the movement keys that change the selection
    movement_keys = {pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1), pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0)}

    def __init__(self, width: int = 6, height: int = 4):

        # super().__init__(title="Memory", dimensions=(600, 300))
        # ensure the given width and height are within parameters

        # TODO: does this include borders? hrm!
        # self.card_width = 30
        # self.card_height = 40

        # card parameters
        # card_border = 2
        # card_sep_x = 10
        # card_sep_y = 10

        px_width = (self.card_margin * 2) + (width * self.card_width) + ((width - 1) * self.card_sep)
        px_height = (self.card_margin * 2) + (height * self.card_height) + ((height - 1) * self.card_sep)

        # hrm... this probably needs to be redone
        # px_width = (self.card_width * width) + (card_sep_x * (width + 1))
        # px_height = (self.card_height * height) + (card_sep_y * (height + 1))

        super().__init__(title="Memory", dimensions=(px_width, px_height), background=color.grey_dark)
        print(px_width, px_height)

        # the card layer, where the cards are displayed
        self.add_layer("cards", dimensions=(px_width, px_height))

        # use whatever system font is available for now, unfortunately
        font = pygame.font.SysFont(None, size=20)

        # create the image of the text desired
        unknown_surface = font.render("?", True, color.black)

        # obtain the dimensions of the winning imagine, so it can be plotted
        unknown_rect = unknown_surface.get_rect()

        unknown_x_mod = int(self.card_width / 2) - int(unknown_rect.width / 2)
        unknown_y_mod = int(self.card_height / 2) - int(unknown_rect.height / 2)

        # store where the cards should be drawn
        self.card_coords = dict()
        for w in range(width):
            for h in range(height):

                # upper left point of each card
                point = (
                    self.card_margin + (w * (self.card_width + self.card_sep)),
                    self.card_margin + (h * (self.card_height + self.card_sep)),
                )
                print(point)

                # store the point where the image is being drawn
                self.card_coords[(w, h)] = point
                # pygame.draw.circle(self.maze_surface, color.green, center=self.point_map[self.goal], radius=5)

                # window.blit(self.surface, dest=self.position)
                # THIS IS BAD
                # self.layers['cards'].blit(create_text_box('?', size=24), dest=point)
                pygame.draw.rect(
                    surface=self.layers["cards"],
                    color=color.red,
                    rect=pygame.Rect(point[0], point[1], self.card_width, self.card_height),
                )

                # write a unknown question mark into the middle
                unknown_point = (point[0] + unknown_x_mod, point[1] + unknown_y_mod)
                self.layers["cards"].blit(unknown_surface, dest=unknown_point)

                # TODO: assign card values here and store them for later use (perhaps from list of random card options)

        # now lets make a 'selection' layer
        # selection_border_width = 2
        # selection_border_radius = 2

        # draw a selection box that shows what we are selecting
        self.select_point = (0, 0)
        self.select_x, self.select_y = self.card_coords[self.select_point]
        print(self.select_x)
        self.select_x -= self.selection_border_width
        self.select_y -= self.selection_border_width
        print(self.select_x)

        self.add_layer(
            "selection",
            position=(self.select_x, self.select_y),
            dimensions=(
                self.card_width + (self.selection_border_width * 2),
                self.card_height + (self.selection_border_width * 2),
            ),
        )
        self.layers["selection"].fill(color.green)

        # self.layers['selection']
        # self.layers['selection'].fill(color.green)
        # pygame.Rect()
        # pygame.draw.rect(
        #     surface=self.layers['selection'],
        #     color=color.green,
        #     rect=pygame.Rect(0, 0, self.card_width + (selection_border_width * 2) + 1, self.card_height + (selection_border_width * 2) + 1),
        #     # rect=pygame.Rect(0, 0, self.card_width, self.card_height),
        #     # border_radius=selection_border_radius
        # )

        # pygame.draw.rect(surface=self.layers['selection'], color=color.transparent, rect=pygame.Rect((selection_border_width, selection_border_width, (5,5)), border_radius=2))
        pygame.draw.rect(
            surface=self.layers["selection"],
            color=color.transparent,
            rect=pygame.Rect(
                self.selection_border_width, self.selection_border_width, self.card_width, self.card_height
            ),
            # rect=pygame.Rect(selection_border_width, selection_border_width, self.card_width, self.card_height),
            border_radius=self.selection_border_radius,
        )

        # pygame.draw.rect(surface=self.layers['selection'], color=color.green, rect=)

        # hrmm..
        # pygame.draw.rect(
        #     surface=self.layers['cards'],
        #     color=color.white,
        #     rect=pygame.Rect(self.points[(w, h)], (self.card_width, self.card_height))
        # )

        # print(self.points[(w, h)])

        # pygame.draw.rect()

        # print('adding layer..')
        # layer = f'card[{w}, {h}]'
        # self.add_layer(f'card[{w}, {h}]', position=self.card_points[(w, h)], surface=create_text_box(text='A'))
        # print(f'Added layer: {layer}')

        # pygame.draw.circle(self.maze_surface, color.green, center=self.point_map[self.goal], radius=5)

        # super().__init__(title="Memory", dimensions=(px_width, px_height))

    def draw_card(self, card_x, card_y, text="?"):
        """Draw a card onto the"""
        px_x = 1

    def handle_key(self, key) -> bool:
        """Change the selection if possible based upon the given key."""
        if key in self.movement_keys:
            return self.handle_movement_keys(key)

        # key not handled, simply return False
        return False

    def handle_movement_key(self, key) -> bool:
        """Handle a movement on the memory board game."""
        # the key is in the movement keys
        # determine whether the selection can be changed
        if (position_mod := self.movement_keys.get(key, None)) is None:
            return False
        position_point = self.select_point[0] + position_mod[0], self.select_point[1] + position_mod[1]

        # remember the card offset
        # if the point is not in the grid, simply return False
        if (select_coords := self.card_coords.get(position_point, None)) is None:
            return False
        select_coords = select_coords[0] - self.selection_border_width, select_coords[1] - self.selection_border_width

        # move layer selection and set the new selection point
        self.select_point = position_point
        super().move("selection", select_coords)
        return True


def main(width: int = 6, height: int = 4) -> int:
    """Play a game of memory."""

    game = Memory()

    # events MUST be handled while iterating or the whole thing will break now
    while game.drawing:

        # handle events
        for event in game.events():

            if event.type == pygame.KEYDOWN:
                game.handle_key(key=event.key)

                # # if an arrow key has been pressed, try to move
                # if event.key in movement_keys:

                #     # try to move to an adjacent point
                #     print('HRM!')
                #     # point_mod = movement_keys[event.key]
                #     # point = maze.point[0] + point_mod[0], maze.point[1] + point_mod[1]
                #     # maze.move(point)

            # print(event)

    # while game.playing:
    #   at the end of every iteration, draw?
    #   for event in game.events():
    #       if not game.playing:
    #           return 0
    # if we make playing a property, we can then draw?

    # time.sleep(5)
    # print("derp derp derp")
    # game.add_layer("another", surface=create_text_box("Another text box!", size=20))
    # game.draw()

    print("sleeping ...")
    time.sleep(2)

    return 0


if __name__ == "__main__":
    sys.exit(main())
