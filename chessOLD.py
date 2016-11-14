import pygame, sys, os, constants
from pygame.locals import *


def main():
    # pygame init and declarations
    pygame.init()
    DISPLAY_SURF = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    pygame.display.set_caption('Chess')
    FPS_CLOCK = pygame.time.Clock()
    # game variables
    black_pieces, white_pieces = generatePieces()
    current_player = 'white'
    selected_piece = None
    # game loop
    while True:
        # event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONUP:
                click_coords = (event.pos[0]/constants.TILE_SIZE, event.pos[1]/constants.TILE_SIZE)
                if event.button == 1 and click_coords[0] < 8:
                    if selected_piece is not None:
                        if click_coords in selected_piece:
                            selected_piece = None
                    else:
                        if current_player == 'black' and click_coords in black_pieces.keys():
                            selected_piece = (click_coords, black_pieces[click_coords])
                        elif current_player == 'white' and selected_piece in white_pieces.keys():
                            selected_piece = (click_coords, white_pieces[click_coords])
                            print 'Piece selected.'
        # drawing to screen
        DISPLAY_SURF.fill(constants.BG_COLOR)
        drawBoardTiles(DISPLAY_SURF)
        drawPieces(DISPLAY_SURF, black_pieces, white_pieces)
        if selected_piece is not None:
            drawSelectionSquare(DISPLAY_SURF, selected_piece)
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


def loadPieceSprite(color, piece):
    if (color == 'white' or color == 'black') and piece in ('pawn', 'rook', 'knight', 'bishop', 'queen', 'king'):
        sprite = pygame.image.load(os.path.join('gfx', color+'_'+piece+'.png')).convert()
        sprite.set_colorkey(constants.ALPHA_COLOR)
    else:
        print str(color) + ', ' + str(piece)
        raise NameError('loadPieceSprite: invalid color or piece name given.')
    return sprite


def drawPieces(display, black, white):
    for coords, piece in black.iteritems():
        piece_image = loadPieceSprite('black', piece)
        piece_rect = Rect(coords[0]*constants.TILE_SIZE, coords[1]*constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE)
        display.blit(piece_image, piece_rect)
    for coords, piece in white.iteritems():
        piece_image = loadPieceSprite('white', piece)
        piece_rect = Rect(coords[0]*constants.TILE_SIZE, coords[1]*constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE)
        display.blit(piece_image, piece_rect)


def drawSelectionSquare(display, selected):
    selection_rect = (selected[0][0]*constants.TILE_SIZE, selected[0][1]*constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE)
    pygame.draw.rect(display, constants.SELECTION_COLOR, selection_rect, constants.SELECTION_SQUARE_WIDTH)


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


def newCurrentPlayer(oldPlayer):
    if oldPlayer == 'white':
        player = 'black'
    elif oldPlayer == 'black':
        player = 'white'
    else:
        raise NameError('newCurrentPlayer(): invalid player given.')
    return player

if __name__ == '__main__':
    main()
