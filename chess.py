import pygame, sys, constants
from pygame.locals import *

def main():
    # pygame init and declarations
    pygame.init()
    DISPLAY_SURF = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    pygame.display.set_caption('Chess')
    FPS_CLOCK = pygame.time.Clock()
    # game variables
    black_pieces, white_pieces = generatePieces()
    # game loop
    while True:
        # event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        # drawing to screen
        # TO DO: if game_mode == INTRO: etc
        drawBoardTiles(DISPLAY_SURF)
        # display update + clock
        pygame.display.update()
        FPS_CLOCK.tick(constants.FPS)

def drawBoardTiles(display):
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                tile_color = constants.SQUARE_DARK_COLOR
            else:
                tile_color = constants.SQUARE_LIGHT_COLOR
            tile_rect = Rect(i*constants.TILE_SIZE, j*constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE)
            pygame.draw.rect(display, tile_color, tile_rect)

def generatePieces():
    black = {}
    white = {}
    for i in range(8):
        black[(i, 1)] = 'pawn'
        white[(i, 6)] = 'pawn'
    black[(0, 0)] = 'rook'
    black[(7, 0)] = 'rook'
    white[(0, 7)] = 'rook'
    white[(7, 7)] = 'rook'
    black[(1, 0)] = 'knight'
    black[(6, 0)] = 'knight'
    white[(1, 7)] = 'knight'
    white[(6, 7)] = 'knight'
    black[(2, 0)] = 'bishop'
    black[(5, 0)] = 'bishop'
    white[(2, 7)] = 'bishop'
    white[(5, 7)] = 'bishop'
    black[(3, 0)] = 'queen'
    black[(4, 0)] = 'king'
    white[(3, 7)] = 'queen'
    white[(4, 7)] = 'king'
    return black, white

if __name__ == '__main__':
    main()
