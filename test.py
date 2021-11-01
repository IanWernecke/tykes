import pygame
import time

pygame.init()
black = 0, 0, 0
white = 255, 255, 255

screen = pygame.display.set_mode((640, 480))
screen.fill(white)

surface = pygame.Surface((100, 100))
for x in range(10):
    for y in range(10):
        # (0, 0), (9, 9) ?
        pygame.draw.rect(
            surface,
            (x * 10, y * 10, (x + y) * 10),
            pygame.Rect(
                (x * 10, y * 10),
                ((x * 10) + 9, (y * 10) + 9)
            )
        )
# pygame.draw.rect(surface, black ,pygame.Rect((10, 10), (30, 30)))

# pygame.draw.rect(surface, ,pygame.Rect((10, 10), (30, 30)))

# blit
screen.blit(source=surface, dest=(10, 10))
pygame.display.flip()


time.sleep(10)
