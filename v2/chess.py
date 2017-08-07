import sys
import os
import pygame
from pygame.locals import *


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 70
LABEL_BORDER_SIZE = 20
LABEL_FONT_SIZE = 12
BORDER_SIZE = (SCREEN_HEIGHT - (TILE_SIZE * 8) - LABEL_BORDER_SIZE) / 2
FPS = 60
BG_COLOR = (150, 75, 32)
BOARD_BG_COLOR = (128, 128, 128)
WHITE_TILE_COLOR = (255, 255, 255)
BLACK_TILE_COLOR = (0, 0, 0)
ALPHA_COLOR = (222, 0, 222)
FILE_LIST = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
PIECE_IMAGE_PATHS = {'wp': 'white_pawn.png', 'wr': 'white_rook.png', 'wn': 'white_knight.png', 'wb': 'white_bishop.png',
                     'wq': 'white_queen.png', 'wk': 'white_king.png', 'bp': 'black_pawn.png', 'br': 'black_rook.png',
                     'bn': 'black_knight.png', 'bb': 'black_bishop.png', 'bq': 'black_queen.png', 'bk': 'black_king.png'
                     }


class GameState:

    def __init__(self):
        self.white_turn = True
        #TODO - the rest of what's needed


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Chess v0.2')
    state = GameState()
    pieces = generate_pieces()
    #sprites = generate_sprites()
    label_font = pygame.font.SysFont('timesnewroman', LABEL_FONT_SIZE)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    pass #TODO - clicking
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    pass #TODO - clicking
        screen.fill(BG_COLOR)
        draw_board(screen, pieces, label_font)
        pygame.display.update()
        clock.tick(FPS)


def convert_notation_coords_to_str(tile_coords):
    assert 0 <= tile_coords[0] <= 7, 'Invalid tile x coord'
    assert 0 <= tile_coords[1] <= 7, 'Invalid tile y coord'
    tile_str = '{}{}'.format(FILE_LIST[tile_coords[0]], tile_coords[1] + 1)
    return tile_str


def convert_notation_str_to_coords(tile_str):
    assert len(tile_str) == 2, 'Invalid tile name'
    assert tile_str[0].lower() in FILE_LIST, 'Invalid tile file (letter)'
    assert 1 <= int(tile_str[1]) <= 8, 'Invalid tile rank (number)'
    x = FILE_LIST.index(tile_str[0])
    y = int(tile_str[1]) - 1
    return (x, y)


def draw_board(draw_surf, pieces_list, font):
    board_size = 8 * TILE_SIZE + LABEL_BORDER_SIZE
    board = pygame.Surface((board_size, board_size))
    board.fill(BOARD_BG_COLOR)
    board_play_rect = pygame.Rect(LABEL_BORDER_SIZE, LABEL_BORDER_SIZE, 8 * TILE_SIZE, 8 * TILE_SIZE)
    board.fill(WHITE_TILE_COLOR, rect=board_play_rect)
    for i in range(8):
        file_surf, file_rect = render_text(FILE_LIST[i].upper(), font)
        file_rect.centerx = LABEL_BORDER_SIZE + TILE_SIZE / 2 + i * TILE_SIZE
        file_rect.centery = LABEL_BORDER_SIZE / 2
        board.blit(file_surf, file_rect)
        rank_surf, rank_rect = render_text(str(i + 1), font)
        rank_rect.centery = LABEL_BORDER_SIZE + TILE_SIZE / 2 + i * TILE_SIZE
        rank_rect.centerx = LABEL_BORDER_SIZE / 2
        board.blit(rank_surf, rank_rect)
        tile_rect = pygame.Rect(LABEL_BORDER_SIZE, LABEL_BORDER_SIZE + i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        if i % 2 == 0:
            tile_rect.left += TILE_SIZE
        for j in range(4):
            pygame.draw.rect(board, BLACK_TILE_COLOR, tile_rect)
            tile_rect.left += 2 * TILE_SIZE
    draw_pieces(board, pieces_list)
    draw_surf.blit(board, (BORDER_SIZE, BORDER_SIZE))


def draw_pieces(board_surf, pieces_dict):
    for tile_name, piece_name in pieces_dict.iteritems():
        print 'Tile: {}, Name: {}'.format(tile_name, piece_name)
        tile_coords = convert_notation_str_to_coords(tile_name)
        image_path = os.path.join('gfx', PIECE_IMAGE_PATHS[piece_name])
        piece_surf = pygame.image.load(image_path).convert()
        piece_surf.set_colorkey(ALPHA_COLOR)
        piece_rect = piece_surf.get_rect()
        piece_rect.left = LABEL_BORDER_SIZE + TILE_SIZE * tile_coords[0]
        piece_rect.top = LABEL_BORDER_SIZE + TILE_SIZE * tile_coords[1]
        board_surf.blit(piece_surf, piece_rect)


def generate_pieces():
    return {'a1': 'wr', 'b1': 'wn', 'c1': 'wb', 'd1': 'wq', 'e1': 'wk', 'f1': 'wb', 'g1': 'wn', 'h1': 'wr',
            'a2': 'wp', 'b2': 'wp', 'c2': 'wp', 'd2': 'wp', 'e2': 'wp', 'f2': 'wp', 'g2': 'wp', 'h2': 'wp',
            'a8': 'br', 'b8': 'bn', 'c8': 'bb', 'd8': 'bq', 'e8': 'bk', 'f8': 'bb', 'g8': 'bn', 'h8': 'br',
            'a7': 'bp', 'b7': 'bp', 'c7': 'bp', 'd7': 'bp', 'e7': 'bp', 'f7': 'bp', 'g7': 'bp', 'h7': 'bp'
            }


def generate_sprites():
    sprite_dict = {}
    #sprite_dict['wp'] = pygame.image.load().convert() #TODO -- do gfx, finish these


def render_text(text, font, color=(0, 0, 0)):
    text_surf = font.render(text, False, color)
    text_rect = text_surf.get_rect()
    return text_surf, text_rect


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
