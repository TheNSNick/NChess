import sys
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
                click_x = event.pos[0] / TILE_SIZE
                click_y = event.pos[1] / TILE_SIZE
                click_coords = (click_x, click_y)
                if board.select_coords is not None:
                    if click_coords == board.select_coords:
                        board.select_coords = None
                    else:
                        select_piece = board[board.select_coords]
                        select_x, select_y = board.select_coords
                        if click_coords in select_piece.attacks(select_x, select_y, board):
                            move_color = board.turn
                            move_text = move_notation(select_piece, board.select_coords, click_coords, capture=True)
                            board[click_coords] = board.pop(board.select_coords)
                            board.select_coords = None
                            board.next_turn()
                            if board.in_check(board.turn):
                                move_text += '+'
                            moves[move_color].append(move_text)
                        elif click_coords in select_piece.free_moves(select_x, select_y, board):
                            move_color = board.turn
                            move_text = move_notation(select_piece, board.select_coords, click_coords)
                            board[click_coords] = board.pop(board.select_coords)
                            board.select_coords = None
                            board.next_turn()
                            if board.in_check(board.turn):
                                move_text += '+'
                            moves[move_color].append(move_text)
                else:
                    if click_coords in board.iterkeys():
                        if board[click_coords].color == board.turn:
                            board.select_coords = click_coords
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

if __name__ == '__main__':
    main()