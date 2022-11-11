# standard imports
import math
import random
import time
from copy import deepcopy

# installed imports
import pygame

# module imports
from tykes import color


def centralize(larger_surface, smaller_surface):
    """Obtain the (x, y) coordinate required to blit the smaller surface onto the center of the larger one."""
    large_x, large_y = larger_surface.get_size()
    small_x, small_y = smaller_surface.get_size()

    return (int(large_x / 2) - int(small_x / 2), int(large_y / 2) - int(small_y / 2))


def neighbors(x: int, y: int, max_width: int, max_height: int):

    # note: max width and max height numbers should never be present in the results

    # if the height is greater than 1, yield (x, height - 1)
    # ^
    if y > 0:
        yield x, y - 1

    # if the width is less than the max width, yield (width  + 1, y)
    # >
    if x < max_width - 1:
        yield x + 1, y

    # if the height is less than the max
    # v
    if y < max_height - 1:
        yield x, y + 1

    # if the width is greater than 0, yield (x - 1, y)
    if x > 0:
        yield x - 1, y


def create_text_box_fixed(
    text, size=12, color=color.black, bg_color=color.white, border=3, border_color=color.black, width=200, height=50
):

    # use whatever system font is available for now, unfortunately
    font = pygame.font.SysFont(None, size)

    # create the image of the text desired
    img = font.render(text, True, color)

    # draw the background
    surface = pygame.Surface((width, height))

    if border > 0:
        surface.fill(border_color)

    draw_inner_rect(surface=surface, color=bg_color, border=border)

    surface.blit(img, centralize(surface, img))
    return surface


def create_text_box(
    text, size=12, color=color.black, margin=10, bg_color=color.white, border=3, border_color=color.black
):

    # use whatever system font is available for now, unfortunately
    font = pygame.font.SysFont(None, size)

    # create the image of the text desired
    img = font.render(text, True, color)

    # obtain the dimensions of the winning imagine, so it can be plotted
    rect = img.get_rect()

    surface_width = rect.width + (margin * 2) + (border * 2)
    surface_height = rect.height + (margin * 2) + (border * 2)

    surface = pygame.Surface((surface_width, surface_height))
    surface.fill(border_color)

    draw_inner_rect(surface=surface, color=bg_color, border=border)

    # draw the text
    img_x = border + margin
    img_y = border + margin
    surface.blit(img, (img_x, img_y))

    # return the entire image
    return surface


def draw_inner_rect(surface, color, border):
    """Draw a rectangle centered on the specified surface, leaving a border."""

    width, height = surface.get_size()

    # draw the background
    bg_x, bg_y = border, border
    bg_width = width - (border * 2)
    bg_height = height - (border * 2)
    return pygame.draw.rect(surface, color, pygame.Rect((bg_x, bg_y), (bg_width, bg_height)))


# TODO: this should be a thread that gets waited upon
def frame_rate(frames_per_second: int):
    """This generator sleeps between intervals of when it is called."""
    frame_interval = 1.0 / frames_per_second
    start_time = time.time()
    while True:

        # calculate the next interval start time
        next_time = start_time + frame_interval

        yield next_time

        # get the current time and if the interval has not yet elapsed, sleep
        end_time = time.time()
        if end_time < next_time:
            time.sleep(next_time - end_time)
            start_time = next_time
        else:
            start_time = end_time


def generate_easy(width: int, height: int) -> list:
    """Create a maze of the specified width and height."""

    points = [(random.randint(0, width - 1), random.randint(0, height - 1))]
    connections = []

    def open_neighbors(x: int, y: int):
        """Return neighbors not already in the points list, and within the maximum ranges."""
        return [
            neighbor for neighbor in neighbors(x=x, y=y, max_width=width, max_height=height) if neighbor not in points
        ]

    # while points within the field have open neighbors, walk them randomly and build a maze
    has_open_neighbors = deepcopy(points)
    while has_open_neighbors:

        # randomly pick one of the points that still have open neighbors
        point = random.choice(has_open_neighbors)

        # get the points open neighbors
        # ensure the specified point still has open neighbors
        point_open_neighbors = open_neighbors(*point)
        if not point_open_neighbors:
            has_open_neighbors.remove(point)
            continue

        # if the point has only one open neighbor, connect and remove from list of points with open neighbors
        if len(point_open_neighbors) == 1:
            neighbor = point_open_neighbors.pop(0)
            has_open_neighbors.remove(point)

        # the point has more than one open neighbor, simply pick one at random
        else:
            neighbor = random_pop(point_open_neighbors)

        # connect the selected neighbor to the point
        points.append(neighbor)
        connections.append((point, neighbor))

        # if the point neighbor has open neighbors, add it to has_open_neighbors
        if any(neighbor not in points for neighbor in neighbors(*neighbor, max_width=width, max_height=height)):
            has_open_neighbors.append(neighbor)

    # return the list of connections from (point_a, point_b)
    return connections


def generate_experiment(width: int, height: int) -> list:
    """Create a maze of the specified width and height."""

    points = [(random.randint(0, width - 1), random.randint(0, height - 1))]
    connections = []

    def open_neighbors(x: int, y: int):
        """Return neighbors not already in the points list, and within the maximum ranges."""
        return [
            neighbor for neighbor in neighbors(x=x, y=y, max_width=width, max_height=height) if neighbor not in points
        ]

    # while points within the field have open neighbors, walk them randomly and build a maze
    has_open_neighbors = deepcopy(points)
    while has_open_neighbors:

        # randomly pick one of the points that still have open neighbors
        # point = random.choice(has_open_neighbors)
        length = len(has_open_neighbors)
        if length == 1:
            point = has_open_neighbors[0]
        else:
            x = math.floor(math.sqrt(length))
            x = math.floor(random.randint(1, x)) * math.floor(random.randint(1, x))
            point = has_open_neighbors[x - 1]

        # get the points open neighbors
        # ensure the specified point still has open neighbors
        point_open_neighbors = open_neighbors(*point)
        if not point_open_neighbors:
            has_open_neighbors.remove(point)
            continue

        # if the point has only one open neighbor, connect and remove from list of points with open neighbors
        if len(point_open_neighbors) == 1:
            neighbor = point_open_neighbors.pop(0)
            has_open_neighbors.remove(point)

        # the point has more than one open neighbor, simply pick one at random
        else:
            neighbor = random_pop(point_open_neighbors)

        # connect the selected neighbor to the point
        points.append(neighbor)
        connections.append((point, neighbor))

        # if the point neighbor has open neighbors, add it to has_open_neighbors
        if any(neighbor not in points for neighbor in neighbors(*neighbor, max_width=width, max_height=height)):
            has_open_neighbors.append(neighbor)

    # return the list of connections from (point_a, point_b)
    return connections


def random_pop(items: list):
    """Pop a random item from the given list."""
    list_len = len(items)
    if list_len == 1:
        return items.pop(0)
    return items.pop(random.randint(1, list_len) - 1)
