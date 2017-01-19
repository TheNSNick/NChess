import sys
import pygame
from pygame.locals import *
import Board02

# constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 75
FPS = 30
BACKGROUND_COLOR = (128, 128, 128)

def main():
    # init
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    board = Board02.Board()
    # game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                click_x = event.pos[0] / TILE_SIZE
                click_y = event.pos[1] / TILE_SIZE
                click_coords = (click_x, click_y)
                if click_coords in board.iterkeys():
                    if board.select_coords is None:
                        if board.tiles[click_coords].color == board.turn:
                            board.select_coords = click_coords
                    elif board.select_coords == click_coords:
                        board.select_coords = None
        # drawing
        screen.fill(BACKGROUND_COLOR)
        board.draw(screen)
        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()