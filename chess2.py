import pygame, sys, os
from pygame.locals import *

# CONSTANTS
# scalars
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 75
FPS = 30
SELECTION_SQUARE_WIDTH = 5
SELECTION_TRAIL_ALPHA = 128
# colors
BG_COLOR = (128, 128, 128)
WHITE_TILE_COLOR = (85, 85, 85)
BLACK_TILE_COLOR = (170, 170, 170)
SELECTION_SQUARE_COLOR = (200, 200, 0)
SELECTION_TRAIL_COLOR = (0, 200, 200)
ALPHA_COLOR = (222, 0, 222)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Chess')
    clock = pygame.time.Clock()
    game_board = new_board()
    current_player = 'white'
    selected_square = None
    # GAME LOOP
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                click_tile = mouse_to_board_coords(event.pos)
                if event.button == 1 and click_tile != (-1, -1):
                    if selected_square is None:
                        if click_tile in game_board.keys():
                            if game_board[click_tile][0] == current_player:
                                selected_square = click_tile
                    else:
                        if click_tile == selected_square:
                            selected_square = None
                        else:
                            if click_tile in valid_moves(selected_square, game_board, current_player):
                                # make move
                                move_piece = game_board[selected_square]
                                game_board[click_tile] = move_piece
                                del game_board[selected_square]
                                if current_player == 'black':
                                    current_player = 'white'
                                elif current_player == 'white':
                                    current_player = 'black'
                                selected_square = None
        screen.fill(BG_COLOR)
        draw_tiles(screen)
        draw_pieces(screen, game_board)
        if selected_square is not None:
            draw_selection_square(screen, selected_square)
            draw_selection_moves(screen, selected_square, game_board, current_player)
        # draw side panel
        pygame.display.update()
        clock.tick(FPS)


def new_board():
    squares = {}
    for i in range(8):
        squares[(i, 1)] = ('black', 'pawn')
        squares[(i, 6)] = ('white', 'pawn')
    squares[0, 0] = ('black', 'rook')
    squares[0, 7] = ('white', 'rook')
    squares[7, 0] = ('black', 'rook')
    squares[7, 7] = ('white', 'rook')
    squares[1, 0] = ('black', 'knight')
    squares[1, 7] = ('white', 'knight')
    squares[6, 0] = ('black', 'knight')
    squares[6, 7] = ('white', 'knight')
    squares[2, 0] = ('black', 'bishop')
    squares[2, 7] = ('white', 'bishop')
    squares[5, 0] = ('black', 'bishop')
    squares[5, 7] = ('white', 'bishop')
    squares[3, 0] = ('black', 'queen')
    squares[3, 7] = ('white', 'queen')
    squares[4, 0] = ('black', 'king')
    squares[4, 7] = ('white', 'king')
    return squares


def draw_tiles(display):
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                tile_color = WHITE_TILE_COLOR
            else:
                tile_color = BLACK_TILE_COLOR
            tile_rect = Rect(i*TILE_SIZE, j*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(display, tile_color, tile_rect)


def mouse_to_board_coords(mouse_coords):
    tile_x = mouse_coords[0] / TILE_SIZE
    tile_y = mouse_coords[1] / TILE_SIZE
    if 0 <= tile_x <= 7 and 0 <= tile_y <= 7:
        return (tile_x, tile_y)
    else:
        return (-1, -1)


def draw_pieces(display, board):
    for coords, piece in board.items():
        file_name = '{}_{}.png'.format(piece[0], piece[1])
        piece_image = pygame.image.load(os.path.join('gfx', file_name)).convert()
        piece_image.set_colorkey(ALPHA_COLOR)
        piece_rect = (coords[0] * TILE_SIZE, coords[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        display.blit(piece_image, piece_rect)


def draw_selection_square(display, coords):
    draw_rect = Rect(coords[0]*TILE_SIZE, coords[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(display, SELECTION_SQUARE_COLOR, draw_rect, SELECTION_SQUARE_WIDTH)


def draw_selection_moves(display, coords, board, player):
    for move in valid_moves(coords, board, player):
        piece_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        piece_image.fill(SELECTION_TRAIL_COLOR)
        piece_image.set_alpha(SELECTION_TRAIL_ALPHA)
        piece_rect = Rect(move[0]*TILE_SIZE, move[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE)
        display.blit(piece_image, piece_rect)


def valid_moves(coords, board, player):
    moves = []
    if coords in board.keys():
        move_piece = board[coords]
        if move_piece[0] == player:
            piece_type = move_piece[1]
    if piece_type == 'pawn':
        moves.extend(pawn_moves(coords, board, player))
    elif piece_type == 'rook':
        moves.extend(orthogonal_moves(coords, board, player))
    elif piece_type == 'knight':
        moves.extend(knight_moves(coords, board, player))
    elif piece_type == 'bishop':
        moves.extend(diagonal_moves(coords, board, player))
    elif piece_type == 'queen':
        moves.extend(orthogonal_moves(coords, board, player))
        moves.extend(diagonal_moves(coords, board, player))
    elif piece_type == 'king':
        moves.extend(king_moves(coords, board, player))
    moves = list(set(moves))
    for move in moves:
        if not is_valid_move(board, player, coords, move):
            moves.remove(move)

    return moves


def pawn_moves(coords, board, player):
    moves = []
    x, y = coords
    if player == 'black':
        direction = 1
        start_row = 1
    elif player == 'white':
        direction = -1
        start_row = 6
    if (x, y + direction) not in board.keys():
        moves.append((x, y + direction))
        if y == start_row:
            if (x, y + 2 * direction) not in board.keys():
                moves.append((x, y + 2 * direction))
    if (x - 1, y + direction) in board.keys():
        if board[(x - 1, y + direction)][0] != player:
            moves.append((x - 1, y + direction))
    if (x + 1, y + direction) in board.keys():
        if board[(x + 1, y + direction)][0] != player:
            moves.append((x + 1, y + direction))
    return moves


def knight_moves(coords, board, player):
    moves = []
    x, y = coords
    if x >= 2:
        if y >= 1:
            # 10 o'clock move
            if (x - 2, y - 1) not in board.keys():
                moves.append((x - 2, y - 1))
            elif board[(x - 2, y - 1)][0] != player:
                moves.append((x - 2, y - 1))
        if y <= 6:
            # 8 o'clock move
            if (x - 2, y + 1) not in board.keys():
                moves.append((x - 2, y + 1))
            elif board[(x - 2, y + 1)][0] != player:
                moves.append((x - 2, y + 1))
    if x <= 5:
        if y >= 1:
            # 2 o'clock move
            if (x + 2, y - 1) not in board.keys():
                moves.append((x + 2, y - 1))
            elif board[(x + 2, y - 1)][0] != player:
                moves.append((x + 2, y - 1))
        if y <= 6:
            # 4 o'clock move
            if (x + 2, y + 1) not in board.keys():
                moves.append((x + 2, y + 1))
            elif board[(x + 2, y + 1)][0] != player:
                moves.append((x + 2, y + 1))
    if y >= 2:
        if x >= 1:
            # 11 o'clock move
            if (x - 1, y - 2) not in board.keys():
                moves.append((x - 1, y - 2))
            elif board[(x - 1, y - 2)][0] != player:
                moves.append((x - 1, y - 2))
        if x <= 6:
            # 1 o'clock move
            if (x + 1, y - 2) not in board.keys():
                moves.append((x + 1, y - 2))
            elif board[(x + 1, y - 2)][0] != player:
                moves.append((x + 1, y - 2))
    if y <= 5:
        if x >= 1:
            # 7 o'clock move
            if (x - 1, y + 2) not in board.keys():
                moves.append((x - 1, y + 2))
            elif board[(x - 1, y + 2)][0] != player:
                moves.append((x - 1, y + 2))
        if x <= 6:
            # 5 o'clock move
            if (x + 1, y + 2) not in board.keys():
                moves.append((x + 1, y + 2))
            elif board[(x + 1, y + 2)][0] != player:
                moves.append((x + 1, y + 2))
    return moves


def orthogonal_moves(coords, board, player):
    moves = []
    x, y = coords
    # up
    for i in range(y):
        if (x, y - i - 1) not in board.keys():
            moves.append((x, y - i - 1))
        else:
            if board[(x, y - i - 1)][0] != player:
                moves.append((x, y - i - 1))
            break
    # down
    for i in range(7-y):
        if (x, y + i + 1) not in board.keys():
            moves.append((x, y + i + 1))
        else:
            if board[(x, y + i + 1)][0] != player:
                moves.append((x, y + i + 1))
            break
    # left
    for i in range(x):
        if (x - i - 1, y) not in board.keys():
            moves.append((x - i - 1, y))
        else:
            if board[(x - i - 1, y)][0] != player:
                moves.append((x - i - 1, y))
            break
    # right
    for i in range(7-x):
        if (x + i + 1, y) not in board.keys():
            moves.append((x + i + 1, y))
        else:
            if board[(x + i + 1, y)][0] != player:
                moves.append((x + i + 1, y))
            break
    return moves


def diagonal_moves(coords, board, player):
    moves = []
    x, y = coords
    # up-left
    for i in range(min(x, y)):
        if (x - i - 1, y - i - 1) not in board.keys():
            moves.append((x - i - 1, y - i - 1))
        else:
            if board[(x - i - 1, y - i - 1)][0] != player:
                moves.append((x - i - 1, y - i - 1))
            break
    # up-right
    for i in range(min(7-x, y)):
        if (x + i + 1, y - i - 1) not in board.keys():
            moves.append((x + i + 1, y - i - 1))
        else:
            if board[(x + i + 1, y - i - 1)][0] != player:
                moves.append((x + i + 1, y - i - 1))
            break
    # down-left
    for i in range(min(x, 7-y)):
        if (x - i - 1, y + i + 1) not in board.keys():
            moves.append((x - i - 1, y + i + 1))
        else:
            if board[(x - i - 1, y + i + 1)][0] != player:
                moves.append((x - i - 1, y + i + 1))
            break
    # down-right
    for i in range(min(7-x, 7-y)):
        if (x + i + 1, y + i + 1) not in board.keys():
            moves.append((x + i + 1, y + i + 1))
        else:
            if board[(x + i + 1, y + i + 1)][0] != player:
                moves.append((x + i + 1, y + i + 1))
            break
    return moves


def king_moves(coords, board, player):
    moves = []
    x, y = coords
    if (x, y - 1) not in board.keys():
        moves.append((x, y - 1))
    elif board[(x, y - 1)][0] != player:
        moves.append((x, y - 1))
    if (x + 1, y - 1) not in board.keys():
        moves.append((x + 1, y - 1))
    elif board[(x + 1, y - 1)][0] != player:
        moves.append((x + 1, y - 1))
    if (x + 1, y) not in board.keys():
        moves.append((x + 1, y))
    elif board[(x + 1, y)][0] != player:
        moves.append((x + 1, y))
    if (x + 1, y + 1) not in board.keys():
        moves.append((x + 1, y + 1))
    elif board[(x + 1, y + 1)][0] != player:
        moves.append((x + 1, y + 1))
    if (x, y + 1) not in board.keys():
        moves.append((x, y + 1))
    elif board[(x, y + 1)][0] != player:
        moves.append((x, y + 1))
    if (x - 1, y + 1) not in board.keys():
        moves.append((x - 1, y + 1))
    elif board[(x - 1, y + 1)][0] != player:
        moves.append((x - 1, y + 1))
    if (x - 1, y) not in board.keys():
        moves.append((x - 1, y))
    elif board[(x - 1, y)][0] != player:
        moves.append((x - 1, y))
    if (x - 1, y - 1) not in board.keys():
        moves.append((x - 1, y - 1))
    elif board[(x - 1, y - 1)][0] != player:
        moves.append((x - 1, y - 1))
    return moves


def in_check(board, player):
    king_x, king_y = (None, None)
    for coords, piece in board.items():
        if piece[0] == player and piece[1] == 'king':
            king_x, king_y = coords
            break
    if player == 'black':
        pawn_direction = 1
    elif player == 'white':
        pawn_direction = -1
    # check for pawn checks
    if (king_x - 1, king_y + pawn_direction) in board.keys():
        if board[(king_x - 1, king_y + pawn_direction)][0] != player and board[(king_x - 1, king_y + pawn_direction)][1] == 'pawn':
            return True
    if (king_x + 1, king_y + pawn_direction) in board.keys():
        if board[(king_x + 1, king_y + pawn_direction)][0] != player and board[(king_x + 1, king_y + pawn_direction)][1] == 'pawn':
            return True
    # check orthogonally
    for i in range(king_y):
        if (king_x, king_y - i - 1) in board.keys():
            if board[(king_x, king_y - i - 1)][0] != player and board[(king_x, king_y - i - 1)][1] == ('rook' or 'queen'):
                return True
            elif board[(king_x, king_y - i - 1)][0] == player:
                break
    for i in range(7-king_y):
        if (king_x, king_y + i + 1) in board.keys():
            if board[(king_x, king_y + i + 1)][0] != player and board[(king_x, king_y + i + 1)][1] == ('rook' or 'queen'):
                return True
            elif board[(king_x, king_y + i + 1)][0] == player:
                break
    for i in range(king_x):
        if (king_x - i - 1, king_y) in board.keys():
            if board[(king_x - i - 1, king_y)][0] != player and board[(king_x - i - 1, king_y)][1] == ('rook' or 'queen'):
                return True
            elif board[(king_x - i - 1, king_y)][0] == player:
                break
    for i in range(7-king_x):
        if (king_x + i + 1, king_y) in board.keys():
            if board[(king_x + i + 1, king_y)][0] != player and board[(king_x + i + 1, king_y)][1] == ('rook' or 'queen'):
                return True
            elif board[(king_x + i + 1, king_y)][0] == player:
                break
    # check diagonally
    for i in range(min(king_x, king_y)):
        if (king_x - i - 1, king_y - i - 1) in board.keys():
            if board[(king_x - i - 1, king_y - i - 1)][0] != player and (board[(king_x - i - 1, king_y - i - 1)][1] == 'bishop' or board[(king_x - i - 1, king_y - i - 1)][1] == 'queen'):
                return True
            elif board[(king_x - i - 1, king_y - i - 1)][0] == player:
                break
    for i in range(min(7-king_x, king_y)):
        if (king_x + i + 1, king_y - i - 1) in board.keys():
            if board[(king_x + i + 1, king_y - i - 1)][0] != player and board[(king_x + i + 1, king_y - i - 1)][1] == ('bishop' or 'queen'):
                return True
            elif board[(king_x + i + 1, king_y - i - 1)][0] == player:
                break
    for i in range(min(king_x, 7-king_y)):
        if (king_x - i - 1, king_y + i + 1) in board.keys():
            if board[(king_x - i - 1, king_y + i + 1)][0] != player and board[(king_x - i - 1, king_y + i + 1)][1] == ('bishop' or 'queen'):
                return True
            elif board[(king_x - i - 1, king_y + i + 1)][0] == player:
                break
    for i in range(min(7-king_x, 7-king_y)):
        if (king_x + i + 1, king_y + i + 1) in board.keys():
            if board[(king_x + i + 1, king_y + i + 1)][0] != player and board[(king_x + i + 1, king_y + i + 1)][1] == ('bishop' or 'queen'):
                return True
            elif board[(king_x + i + 1, king_y + i + 1)][0] == player:
                break
    # check knights
    if (king_x + 1, king_y - 2) in board.keys():
        if board[(king_x + 1, king_y - 2)][0] != player and board[(king_x + 1, king_y - 2)][1] == 'knight':
            return True
    if (king_x + 2, king_y - 1) in board.keys():
        if board[(king_x + 2, king_y - 1)][0] != player and board[(king_x + 2, king_y - 1)][1] == 'knight':
            return True
    if (king_x + 2, king_y + 1) in board.keys():
        if board[(king_x + 2, king_y + 1)][0] != player and board[(king_x + 2, king_y + 1)][1] == 'knight':
            return True
    if (king_x + 1, king_y + 2) in board.keys():
        if board[(king_x + 1, king_y + 2)][0] != player and board[(king_x + 1, king_y + 2)][1] == 'knight':
            return True
    if (king_x - 1, king_y + 2) in board.keys():
        if board[(king_x - 1, king_y + 2)][0] != player and board[(king_x - 1, king_y + 2)][1] == 'knight':
            return True
    if (king_x - 2, king_y + 1) in board.keys():
        if board[(king_x - 2, king_y + 1)][0] != player and board[(king_x - 2, king_y + 1)][1] == 'knight':
            return True
    if (king_x - 2, king_y - 1) in board.keys():
        if board[(king_x - 2, king_y - 1)][0] != player and board[(king_x - 2, king_y - 1)][1] == 'knight':
            return True
    if (king_x - 1, king_y - 2) in board.keys():
        if board[(king_x - 1, king_y - 2)][0] != player and board[(king_x - 1, king_y - 2)][1] == 'knight':
            return True
    # check king
    if (king_x, king_y - 1) in board.keys():
        if board[(king_x, king_y - 1)][0] != player and board[(king_x, king_y - 1)][1] == 'king':
            return True
    if (king_x + 1, king_y - 1) in board.keys():
        if board[(king_x + 1, king_y - 1)][0] != player and board[(king_x + 1, king_y - 1)][1] == 'king':
            return True
    if (king_x + 1, king_y) in board.keys():
        if board[(king_x + 1, king_y)][0] != player and board[(king_x + 1, king_y)][1] == 'king':
            return True
    if (king_x + 1, king_y + 1) in board.keys():
        if board[(king_x + 1, king_y + 1)][0] != player and board[(king_x + 1, king_y + 1)][1] == 'king':
            return True
    if (king_x, king_y + 1) in board.keys():
        if board[(king_x, king_y + 1)][0] != player and board[(king_x, king_y + 1)][1] == 'king':
            return True
    if (king_x - 1, king_y + 1) in board.keys():
        if board[(king_x - 1, king_y + 1)][0] != player and board[(king_x - 1, king_y + 1)][1] == 'king':
            return True
    if (king_x - 1, king_y) in board.keys():
        if board[(king_x - 1, king_y)][0] != player and board[(king_x - 1, king_y)][1] == 'king':
            return True
    if (king_x - 1, king_y - 1) in board.keys():
        if board[(king_x - 1, king_y - 1)][0] != player and board[(king_x - 1, king_y - 1)][1] == 'king':
            return True
    return False


def is_valid_move(board, player, from_coords, to_coords):
    if min(to_coords) < 0 or max(to_coords) > 7:
        return False
    check_board = board.copy()
    check_board[to_coords] = board[from_coords]
    del check_board[from_coords]
    return not in_check(check_board, player)

if __name__ == '__main__':
    main()
