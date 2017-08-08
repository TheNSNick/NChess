import sys
import pygame
from pygame.locals import *


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 70
LABEL_BORDER_SIZE = 20
BORDER_SIZE = (SCREEN_HEIGHT - (8 * TILE_SIZE) - LABEL_BORDER_SIZE) / 2
FPS = 60
BG_COLOR = (150, 75, 32)
WHITE_TILE_COLOR = (255, 255, 255)
BLACK_TILE_COLOR = (0, 0, 0)
IMAGES = {'wp': None, 'wr': None, 'wn': None, 'wb': None, 'wq': None, 'wk': None,
          'bp': None, 'br': None, 'bn': None, 'bb': None, 'bq': None, 'bk': None}


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
