import os
import sys
from datetime import datetime
import pygame
from pygame.locals import *
import Board02
import Piece02

# constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 75
FPS = 30
BACKGROUND_COLOR = (128, 128, 128)
RANK_NAMES = 'abcdefgh'
MOVE_TEXT_SIZE = 18
COLORS = {'BLACK': (0, 0, 0), 'WHITE': (255, 255, 255)}

def main():
    # init
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('NChess v0.2')
    clock = pygame.time.Clock()
    board = Board02.Board()
    moves = {'BLACK': [], 'WHITE': []}
    # game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                click_board(screen, board, moves, event.pos, clock)
        # drawing
        screen.fill(BACKGROUND_COLOR)
        board.draw(screen)
        draw_moves(screen, moves)
        pygame.display.update()
        clock.tick(FPS)


def draw_moves(display, move_dict):
    offset = 0
    if len(move_dict['BLACK']) > 18:
        if len(move_dict['BLACK']) % 2 == 1:
            num_grab = 17
        else:
            num_grab = 18
        offset = len(move_dict['BLACK']) - num_grab
        draw_list = move_dict['BLACK'][-num_grab:]
    else:
        draw_list = move_dict['BLACK']
    for i, move in enumerate(draw_list):
        move_text = '{}. {}'.format(i + offset + 1, move)
        move_x = 8 * TILE_SIZE + (i % 2) * ((SCREEN_WIDTH - 8 * TILE_SIZE) / 2) + 10
        move_y = (i / 2) * 20 + 10
        move_surf = render_text(move_text, 'BLACK')
        display.blit(move_surf, (move_x, move_y))
    offset = 0
    if len(move_dict['WHITE']) > 18:
        if len(move_dict['WHITE']) % 2 == 1:
            num_grab = 17
        else:
            num_grab = 18
        offset = len(move_dict['WHITE']) - num_grab
        draw_list = move_dict['WHITE'][-num_grab:]
    else:
        draw_list = move_dict['WHITE']
    for i, move in enumerate(draw_list):
        move_text = '{}. {}'.format(i + offset + 1, move)
        move_x = 8 * TILE_SIZE + (i % 2) * ((SCREEN_WIDTH - 8 * TILE_SIZE) / 2) + 10
        move_y = 5 * TILE_SIZE + (i / 2) * 20 + 10
        move_surf = render_text(move_text, 'WHITE')
        display.blit(move_surf, (move_x, move_y))

'''
def draw_pawn_promotion(display, promote_color):
    promote_surface = pygame.Surface((3 * TILE_SIZE, 3 * TILE_SIZE))
    promote_surface.fill(BACKGROUND_COLOR)
    file_suffixes = ['_rook.png', '_knight.png', '_bishop.png', '_queen.png']
    for i, suffix in enumerate(file_suffixes):
        file_name = os.path.join('gfx', '{}{}'.format(promote_color.lower(), suffix))
        piece_image = pygame.image.load(file_name).convert()
        piece_rect = piece_image.get_rect()
        piece_rect.centerx = ((i % 2) + 1) * (TILE_SIZE + TILE_SIZE / 3)
        if i < 2:
            piece_rect.centery = TILE_SIZE + TILE_SIZE / 3
        else:
            piece_rect.centery = 2 * (TILE_SIZE + TILE_SIZE / 3)
        promote_surface.blit(piece_image, piece_rect)
    display.blit(promote_surface, (5 * TILE_SIZE / 2, 5 * TILE_SIZE / 2))
'''

def click_board(display, board, moves, click_coords, clock):
                click_x = click_coords[0] / TILE_SIZE
                click_y = click_coords[1] / TILE_SIZE
                click_coords = (click_x, click_y)
                if board.select_coords is not None:
                    if click_coords == board.select_coords:
                        board.select_coords = None
                    else:
                        select_piece = board[board.select_coords]
                        select_x, select_y = board.select_coords
                        if click_coords in select_piece.attacks(select_x, select_y, board):
                            move_color = board.turn
                            if not board.flags[board.turn]['king_moved'] and isinstance(select_piece, Piece02.King):
                                board.flags[board.turn]['king_moved'] = True
                            if not board.flags[board.turn]['left_rook_moved'] and isinstance(select_piece, Piece02.Rook) and select_x == 0:
                                board.flags[board.turn]['left_rook_moved'] = True
                            if not board.flags[board.turn]['right_rook_moved'] and isinstance(select_piece, Piece02.Rook) and select_x == 7:
                                board.flags[board.turn]['right_rook_moved'] = True
                            if isinstance(select_piece, Piece02.Pawn) and click_coords not in board.iterkeys():
                                # en passant take -- remove Pawn jumped behind
                                if (click_x, click_y - select_piece.direction()) in board.iterkeys():
                                    _ = board.pop((click_x, click_y - select_piece.direction()))
                            if isinstance(select_piece, Piece02.Pawn) and (click_y == 0 or click_y == 7):
                                # pawn promotion
                                place_piece = None
                                while place_piece is None:
                                    board.draw(display)
                                    board.draw_pawn_promotion(display, board.turn)
                                    for event in pygame.event.get():
                                        if event.type == MOUSEBUTTONDOWN:
                                            if TILE_SIZE / 3 <= event.pos[0] - 5 * TILE_SIZE / 2 <= 4 * TILE_SIZE / 3:
                                                if TILE_SIZE / 3 <= event.pos[1] - 5 * TILE_SIZE / 2 <= 3 * TILE_SIZE / 3:
                                                    place_piece = Piece02.Rook(board.turn)
                                                    text_add = 'R'
                                                elif 5 * TILE_SIZE / 3 <= event.pos[1] - 5 * TILE_SIZE / 2 <= 8 * TILE_SIZE / 3:
                                                    place_piece = Piece02.Knight(board.turn)
                                                    text_add = 'N'
                                            elif 5 * TILE_SIZE / 3 <= event.pos[0] - 5 * TILE_SIZE / 2 <= 8 * TILE_SIZE / 3:
                                                if TILE_SIZE / 3 <= event.pos[1] - 5 * TILE_SIZE / 2 <= 3 * TILE_SIZE / 3:
                                                    place_piece = Piece02.Bishop(board.turn)
                                                    text_add = 'B'
                                                elif 5 * TILE_SIZE / 3 <= event.pos[1] - 5 * TILE_SIZE / 2 <= 8 * TILE_SIZE / 3:
                                                    place_piece = Piece02.Queen(board.turn)
                                                    text_add = 'Q'
                                    pygame.display.update()
                                    clock.tick(FPS)
                                move_text = move_notation(select_piece, board.select_coords, click_coords, capture=True)[:-1]
                                move_text += text_add
                                del board[board.select_coords]
                                board[click_coords] = place_piece
                            else:
                                move_text = move_notation(select_piece, board.select_coords, click_coords, capture=True)
                                board[click_coords] = board.pop(board.select_coords)
                            board.select_coords = None
                            board.next_turn()
                            if board.in_check(board.turn):
                                if board.in_mate(board.turn):
                                    move_text += '#'
                                else:
                                    move_text += '+'
                            moves[move_color].append(move_text)
                        elif click_coords in select_piece.free_moves(select_x, select_y, board):
                            move_color = board.turn
                            if not board.flags[board.turn]['king_moved'] and isinstance(select_piece, Piece02.King):
                                board.flags[board.turn]['king_moved'] = True
                            if not board.flags[board.turn]['left_rook_moved'] and isinstance(select_piece, Piece02.Rook) and select_x == 0:
                                board.flags[board.turn]['left_rook_moved'] = True
                            if not board.flags[board.turn]['right_rook_moved'] and isinstance(select_piece, Piece02.Rook) and select_x == 7:
                                board.flags[board.turn]['right_rook_moved'] = True
                            if isinstance(select_piece, Piece02.Pawn) and (click_y - select_y == 2 or select_y - click_y == 2):
                                board.flags[board.turn]['pawn_jumped'] = click_x
                            else:
                                board.flags[board.turn]['pawn_jumped'] = None
                            if isinstance(select_piece, Piece02.Pawn) and (click_y == 0 or click_y == 7):
                                # pawn promotion
                                place_piece = None
                                while place_piece is None:
                                    board.draw(display)
                                    board.draw_pawn_promotion(display, board.turn)
                                    for event in pygame.event.get():
                                        if event.type == MOUSEBUTTONDOWN:
                                            if TILE_SIZE / 3 <= event.pos[0] - 5 * TILE_SIZE / 2 <= 4 * TILE_SIZE / 3:
                                                if TILE_SIZE / 3 <= event.pos[1] - 5 * TILE_SIZE / 2 <= 3 * TILE_SIZE / 3:
                                                    place_piece = Piece02.Rook(board.turn)
                                                    text_add = 'R'
                                                elif 5 * TILE_SIZE / 3 <= event.pos[1] - 5 * TILE_SIZE / 2 <= 8 * TILE_SIZE / 3:
                                                    place_piece = Piece02.Bishop(board.turn)
                                                    text_add = 'B'
                                            elif 5 * TILE_SIZE / 3 <= event.pos[0] - 5 * TILE_SIZE / 2 <= 8 * TILE_SIZE / 3:
                                                if TILE_SIZE / 3 <= event.pos[1] - 5 * TILE_SIZE / 2 <= 3 * TILE_SIZE / 3:
                                                    place_piece = Piece02.Knight(board.turn)
                                                    text_add = 'N'
                                                elif 5 * TILE_SIZE / 3 <= event.pos[1] - 5 * TILE_SIZE / 2 <= 8 * TILE_SIZE / 3:
                                                    place_piece = Piece02.Queen(board.turn)
                                                    text_add = 'Q'
                                    pygame.display.update()
                                    clock.tick(FPS)
                                move_text = move_notation(select_piece, board.select_coords, click_coords)[:-1]
                                move_text += text_add
                                del board[board.select_coords]
                                board[click_coords] = place_piece
                            else:
                                move_text = move_notation(select_piece, board.select_coords, click_coords)
                                board[click_coords] = board.pop(board.select_coords)
                            if isinstance(select_piece, Piece02.King) and (click_x - select_x == 2 or select_x - click_x == 2):
                                if click_x == 2:
                                    rook_from = (0, click_y)
                                    rook_to = (3, click_y)
                                elif click_x == 6:
                                    rook_from = (7, click_y)
                                    rook_to = (5, click_y)
                                board[rook_to] = board.pop(rook_from)
                            board.select_coords = None
                            board.next_turn()
                            if board.in_check(board.turn):
                                if board.in_mate(board.turn):
                                    move_text += '#'
                                else:
                                    move_text += '+'
                            if 'Kg' in move_text:
                                move_text = '0-0'
                            elif 'Kc' in move_text:
                                move_text = '0-0-0'
                            moves[move_color].append(move_text)
                else:
                    if click_coords in board.iterkeys():
                        if board[click_coords].color == board.turn:
                            board.select_coords = click_coords


def move_notation(piece, from_coords, to_coords, capture=False):
    move = ''
    piece_name = notation_piece_name(piece)
    if piece_name is not None:
        move += piece_name
    if capture:
        if len(move) == 0:
            move += notation_tile_name(from_coords)[0]
        move += 'x'
    move += notation_tile_name(to_coords)
    return str(move)


def notation_piece_name(piece):
    if isinstance(piece, Piece02.Pawn):
        return None
    elif isinstance(piece, Piece02.Rook):
        return 'R'
    elif isinstance(piece, Piece02.Knight):
        return 'N'
    elif isinstance(piece, Piece02.Bishop):
        return 'B'
    elif isinstance(piece, Piece02.Queen):
        return 'Q'
    elif isinstance(piece, Piece02.King):
        return 'K'


def notation_tile_name(coords):
    return '{}{}'.format(RANK_NAMES[coords[0]], coords[1] + 1)


def render_text(text, color):
    m_font = pygame.font.SysFont('arial', MOVE_TEXT_SIZE)
    return m_font.render(text, False, COLORS[color])


def save_game(move_dict):
    file_name = str(datetime.now())
    for char in ' .-:':
        file_name = file_name.replace(char, '')
    file_path = os.path.join('games', '{}.txt'.format(file_name))
    with open(file_path, 'w') as write_file:
        move_num = 1
        for white, black in zip(move_dict['WHITE'], move_dict['BLACK']):
            line = '{}.\t{}\t{}\n'.format(move_num, white, black)
            write_file.write(line)
            move_num += 1
        if len(move_dict['WHITE']) > len(move_dict['BLACK']):
            line = '{}.\t{}\n'.format(move_dict['WHITE'][-1])
            write_file.write(line)

if __name__ == '__main__':
    main()