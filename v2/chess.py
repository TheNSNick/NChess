import sys
import pygame
from pygame.locals import *


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = SCREEN_HEIGHT / 8
FPS = 60
BG_COLOR = (150, 75, 32)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    while True:
        for _ in pygame.event.get(QUIT):
            terminate()
        screen.fill(BG_COLOR)
        pygame.display.update()
        clock.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
