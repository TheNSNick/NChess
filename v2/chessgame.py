import chessfunctions as chess
import os
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
BOARD_BG_COLOR = (128, 128, 128)
WHITE_TILE_COLOR = (255, 255, 255)
BLACK_TILE_COLOR = (0, 0, 0)
ALPHA_COLOR = (222, 0, 222)
SELECTION_SQUARE_COLOR = (200, 200, 0)
SELECTION_MOVE_COLOR = (0, 200, 200)
SELECTION_ATTACK_COLOR = (200, 0, 0)
SELECTION_SQUARE_WIDTH = 5
SELECTION_ALPHA = 128
LABEL_FONT_SIZE = 14


class GameState:

    def __init__(self):
        self.turn = 'w'
        self.pieces = chess.generate_new_pieces()
        self.selected = None
        self.move_list = []
        self.graveyard = []

    def change_turn(self):
        if self.turn == 'w':
            self.turn = 'b'
        elif self.turn == 'b':
            self.turn = 'w'
        else:
            raise ValueError('GameState.change_turn(): self.turn has an invalid value.')


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('NChess v0.2')
    clock = pygame.time.Clock()
    images = {'wp': None, 'wr': None, 'wn': None, 'wb': None, 'wq': None, 'wk': None,
              'bp': None, 'br': None, 'bn': None, 'bb': None, 'bq': None, 'bk': None}
    for piece_name in images.keys():
        image_path = os.path.join('gfx', '{}.png'.format(piece_name))
        image_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        image_surf.blit(pygame.image.load(image_path).convert(), (-2, -2))
        image_surf.set_colorkey(ALPHA_COLOR)
        images[piece_name] = image_surf
    state = GameState()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == MOUSEBUTTONDOWN:
                click_coords = convert_screen_coords_to_board_coords(event.pos)
                if click_coords is not None:
                    if state.selected is None:
                        if click_coords in state.pieces.keys():
                            if state.pieces[click_coords][0] == state.turn:
                                state.selected = click_coords
                    else:
                        if click_coords == state.selected:
                            state.selected = None
                        else:
                            #TODO -- en passant and castling
                            if click_coords in chess.return_moves(state.selected, state.pieces):
                                if click_coords in state.pieces.keys():
                                    state.graveyard.append(state.pieces.pop(click_coords))
                                chess.move_piece(state.selected, click_coords, state.pieces)
                                state.selected = None
                                # TODO -- checkmate and stalemate
                                state.change_turn()
        screen.fill(BG_COLOR)
        draw_board(screen, state.pieces, images)
        if state.selected is not None:
            draw_selection_square(screen, state.selected)
            for move in chess.return_moves(state.selected, state.pieces):
                if move in state.pieces.keys():
                    draw_attack_square(screen, move)
                else:
                    draw_move_square(screen, move)
        pygame.display.update()
        #TESTING
        if chess.in_check('w', state.pieces):
            print ('White in check!')
        elif chess.in_check('b', state.pieces):
            print ('Black in check!')
        clock.tick(FPS)


def convert_screen_coords_to_board_coords(screen_coords):
    screen_x, screen_y = screen_coords
    screen_x -= BORDER_SIZE + LABEL_BORDER_SIZE
    screen_y -= BORDER_SIZE + LABEL_BORDER_SIZE
    if (0 <= screen_x <= 8 * TILE_SIZE) and (0 <= screen_y <= 8 * TILE_SIZE):
        board_x = screen_x / TILE_SIZE
        board_y = screen_y / TILE_SIZE
        return (board_x, board_y)
    return None


def draw_board(draw_surf, piece_dict, image_dict):
    board_size = LABEL_BORDER_SIZE + 8 * TILE_SIZE
    board_surf = pygame.Surface((board_size, board_size))
    board_surf.fill(BOARD_BG_COLOR)
    board_rect = Rect(LABEL_BORDER_SIZE, LABEL_BORDER_SIZE, 8 * TILE_SIZE, 8 * TILE_SIZE)
    pygame.draw.rect(board_surf, WHITE_TILE_COLOR, board_rect)
    for y in range(8):
        tile_rect = Rect(LABEL_BORDER_SIZE, (y * TILE_SIZE) + LABEL_BORDER_SIZE, TILE_SIZE, TILE_SIZE)
        if y % 2 == 0:
            tile_rect.left += TILE_SIZE
        for x in range(4):
            pygame.draw.rect(board_surf, BLACK_TILE_COLOR, tile_rect)
            tile_rect.left += 2 * TILE_SIZE
    file_labels = 'ABCDEFGH'
    label_font = pygame.font.SysFont('timesnewroman', LABEL_FONT_SIZE, bold=True)
    for i in range(8):
        file_surf, file_rect = render_text(file_labels[i], label_font)
        file_rect.centerx = LABEL_BORDER_SIZE + TILE_SIZE / 2 + i * TILE_SIZE
        file_rect.centery = LABEL_BORDER_SIZE / 2
        board_surf.blit(file_surf, file_rect)
        rank_surf, rank_rect = render_text(str(i+1), label_font)
        rank_rect.centerx = LABEL_BORDER_SIZE / 2
        rank_rect.centery = LABEL_BORDER_SIZE + TILE_SIZE / 2 + i * TILE_SIZE
        board_surf.blit(rank_surf, rank_rect)
    for coords, piece_name in piece_dict.iteritems():
        assert piece_name in image_dict.iterkeys(), 'draw_board: {} not found in images keys'.format(piece_name)
        piece_surf = image_dict[piece_name]
        piece_rect = piece_surf.get_rect()
        piece_rect.left = LABEL_BORDER_SIZE + coords[0] * TILE_SIZE
        piece_rect.top = LABEL_BORDER_SIZE + coords[1] * TILE_SIZE
        board_surf.blit(piece_surf, piece_rect)
    draw_surf.blit(board_surf, (BORDER_SIZE, BORDER_SIZE))


def draw_attack_square(draw_surf, attack_coords):
    square_x = BORDER_SIZE + LABEL_BORDER_SIZE + attack_coords[0] * TILE_SIZE
    square_y = BORDER_SIZE + LABEL_BORDER_SIZE + attack_coords[1] * TILE_SIZE
    square_rect = Rect(square_x, square_y, TILE_SIZE, TILE_SIZE)
    square_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
    square_surf.fill(SELECTION_ATTACK_COLOR)
    square_surf.set_alpha(SELECTION_ALPHA)
    draw_surf.blit(square_surf, square_rect)


def draw_move_square(draw_surf, move_coords):
    square_x = BORDER_SIZE + LABEL_BORDER_SIZE + move_coords[0] * TILE_SIZE
    square_y = BORDER_SIZE + LABEL_BORDER_SIZE + move_coords[1] * TILE_SIZE
    square_rect = Rect(square_x, square_y, TILE_SIZE, TILE_SIZE)
    square_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
    square_surf.fill(SELECTION_MOVE_COLOR)
    square_surf.set_alpha(SELECTION_ALPHA)
    draw_surf.blit(square_surf, square_rect)


def draw_selection_square(draw_surf, select_coords):
    square_x = BORDER_SIZE + LABEL_BORDER_SIZE + select_coords[0] * TILE_SIZE
    square_y = BORDER_SIZE + LABEL_BORDER_SIZE + select_coords[1] * TILE_SIZE
    square_rect = Rect(square_x, square_y, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(draw_surf, SELECTION_SQUARE_COLOR, square_rect, SELECTION_SQUARE_WIDTH)


def render_text(text, font, color=(0, 0, 0)):
    text_surf = font.render(text, False, color)
    text_rect = text_surf.get_rect()
    return text_surf, text_rect


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()