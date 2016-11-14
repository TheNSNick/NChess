import sys, pygame, os
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
WHITE_SQUARE_COLOR = (85, 85, 85)
BLACK_SQUARE_COLOR = (170, 170, 170)
SELECTION_SQUARE_COLOR = (200, 200, 0)
SELECTION_TRAIL_COLOR = (0, 200, 200)
ALPHA_COLOR = (222, 0, 222)


def main():
    pygame.init()
    display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    tick_clock = pygame.time.Clock()
    board = generate_test_board()
    selected_coords = None
    selected_piece = None
    current_player = 'white'
    # main loop
    while True:
        display_surface.fill(BG_COLOR)
        # event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                click_coords = screen_xy_to_board_xy(event.pos)
                if selected_piece is None and click_coords != (-1, -1):
                    if click_coords in board.keys():
                        color, type = board[click_coords].split()
                        if color == current_player:
                            selected_coords = click_coords
                            selected_piece = board[click_coords]
                elif selected_piece is not None and click_coords != (-1, -1):
                    if click_coords == selected_coords:
                        selected_coords = None
                        selected_piece = None
        # display & clock updating
        draw_tiles(display_surface)
        for coords, piece in board.iteritems():
            draw_piece(display_surface, piece, coords)
        if selected_coords is not None:
            draw_selection_square(display_surface, selected_coords)
            draw_selection_trail(display_surface, selected_coords, board)
        if is_in_check(current_player, board):
            pygame.display.set_caption('CHECK!')
        else:
            pygame.display.set_caption('Chess')
        pygame.display.update()
        tick_clock.tick(FPS)


def draw_tiles(display):
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                tile_color = WHITE_SQUARE_COLOR
            else:
                tile_color = BLACK_SQUARE_COLOR
            tile_rect = Rect(i*TILE_SIZE, j*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(display, tile_color, tile_rect)


def draw_piece(display, piece, coords):
    color, type = piece.split()
    file_name = color + '_' + type + '.png'
    image = pygame.image.load(os.path.join('gfx', file_name)).convert()
    image.set_colorkey(ALPHA_COLOR)
    rect = Rect(coords[0]*TILE_SIZE, coords[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE)
    display.blit(image, rect)


def draw_selection_square(display, coords):
    draw_rect = Rect(coords[0]*TILE_SIZE, coords[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(display, SELECTION_SQUARE_COLOR, draw_rect, SELECTION_SQUARE_WIDTH)


def draw_selection_trail(display, coords, board):
    move_squares = return_moves(coords, board)
    if len(move_squares) > 0:
        for square in move_squares:
            image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            image.fill(SELECTION_TRAIL_COLOR)
            image.set_alpha(SELECTION_TRAIL_ALPHA)
            rect = Rect(square[0]*TILE_SIZE, square[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            display.blit(image, rect)


def generate_board():
    new_board = {}
    for i in range(8):
        new_board[(i, 1)] = 'black pawn'
        new_board[(i, 6)] = 'white pawn'
    new_board[(0, 0)] = 'black rook'
    new_board[(7, 0)] = 'black rook'
    new_board[(1, 0)] = 'black knight'
    new_board[(6, 0)] = 'black knight'
    new_board[(2, 0)] = 'black bishop'
    new_board[(5, 0)] = 'black bishop'
    new_board[(3, 0)] = 'black queen'
    new_board[(4, 0)] = 'black king'
    new_board[(0, 7)] = 'white rook'
    new_board[(7, 7)] = 'white rook'
    new_board[(1, 7)] = 'white knight'
    new_board[(6, 7)] = 'white knight'
    new_board[(2, 7)] = 'white bishop'
    new_board[(5, 7)] = 'white bishop'
    new_board[(3, 7)] = 'white queen'
    new_board[(4, 7)] = 'white king'
    return new_board


def generate_test_board():
    new_board = {}
    new_board[(5, 2)] = 'white pawn'
    new_board[(6, 3)] = 'white pawn'
    new_board[(6, 5)] = 'white pawn'
    new_board[(5, 6)] = 'white pawn'
    new_board[(3, 6)] = 'white pawn'
    new_board[(2, 5)] = 'white pawn'
    new_board[(2, 3)] = 'white pawn'
    new_board[(3, 2)] = 'white pawn'
    new_board[(4, 4)] = 'white knight'
    new_board[(7, 7)] = 'white king'
    return new_board


def screen_xy_to_board_xy(screen_coords):
    board_coords = (screen_coords[0]/TILE_SIZE, screen_coords[1]/TILE_SIZE)
    if max(board_coords) > 7 or min(board_coords) < 0:
        return -1, -1
    else:
        return board_coords


def change_player(player):
    if player == 'white':
        return 'black'
    elif player == 'black':
        return 'white'
    else:
        raise NameError('change_player(): Invalid player given.')


def return_moves(coords, board):
    if coords in board.keys():
        move_piece = board[coords]
    else:
        raise NameError('return_moves(): Invalid coords given.')
    _, move_type = move_piece.split()
    if move_type == 'pawn':
        return pawn_moves(coords, board)
    elif move_type == 'rook':
        return rook_moves(coords, board)
    elif move_type == 'knight':
        return knight_moves(coords, board)
    '''
    elif move_type == 'bishop':
        return bishop_moves(coords, board)
    elif move_type == 'queen':
        return queen_moves(coords, board)
    elif move_type == 'king':
        return king_moves(coords, board)
    else:
        raise NameError('return_moves(): Invalid piece type found.')
    '''


def pawn_moves(coords, board):
    moves = []
    move_piece = board[coords]
    piece_color, _ = move_piece.split()
    if piece_color == 'black':
        direction = 1
    elif piece_color == 'white':
        direction = -1
    else:
        raise NameError('pawn_moves(): Pawn has invalid color.')
    piece_x, piece_y = coords
    one_ahead = False
    check_worry = False
    temp_board = board.copy()
    del temp_board[coords]
    if is_in_check(piece_color, temp_board):
        check_worry = True
        temp_board = board.copy()
        del temp_board[coords]
    if (piece_x, piece_y+direction) not in board.keys():
        if not check_worry:
            moves.append((piece_x, piece_y+direction))
            one_ahead = True
        else:
            temp_board[(piece_x, piece_y+direction)] = move_piece
            if not is_in_check(piece_color, temp_board):
                moves.append((piece_x, piece_y+direction))
                one_ahead = True
                temp_board = board.copy()
                del temp_board[coords]
    if one_ahead and (piece_x, piece_y+2*direction) not in board.keys() and ((piece_color == 'black' and piece_y == 1) or (piece_color == 'white' and piece_y == 6)):
        if not check_worry:
            moves.append((piece_x, piece_y+2*direction))
        else:
            temp_board[(piece_x, piece_y+2*direction)] = move_piece
            if not is_in_check(piece_color, temp_board):
                moves.append((piece_x, piece_y+2*direction))
                temp_board = board.copy()
                del temp_board[coords]
    if piece_x > 0:
        if (piece_x-1, piece_y+direction) in board.keys():
            other_color, _ = board[(piece_x-1, piece_y+direction)].split()
            if piece_color != other_color:
                if not check_worry:
                    moves.append((piece_x-1, piece_y+direction))
                else:
                    temp_board[(piece_x-1, piece_y+direction)] = move_piece
                    if not is_in_check(piece_color, temp_board):
                        moves.append((piece_x-1, piece_y+direction))
                        temp_board = board.copy()
                        del temp_board[coords]
    if piece_x < 7:
        if (piece_x+1, piece_y+direction) in board.keys():
            other_color, _ = board[(piece_x+1, piece_y+direction)].split()
            if other_color != piece_color:
                if not check_worry:
                    moves.append((piece_x+1, piece_y+direction))
                else:
                    temp_board[(piece_x-1, piece_y+direction)] = move_piece
                    if not is_in_check(piece_color, temp_board):
                        moves.append((piece_x+1, piece_y+direction))
    return moves


def rook_moves(coords, board):
    moves = []
    move_piece = board[coords]
    piece_color, _ = move_piece.split()
    piece_x, piece_y = coords
    check_worry = False
    temp_board = board.copy()
    del temp_board[coords]
    if is_in_check(piece_color, temp_board):
        check_worry = True
    for i in range(piece_x):
        if (piece_x-i-1, piece_y) not in board.keys():
            if not check_worry:
                moves.append((piece_x-i-1, piece_y))
            else:
                temp_board = board.copy()
                del temp_board[coords]
                temp_board[(piece_x-i-1, piece_y)] = move_piece
                if not is_in_check(piece_color, temp_board):
                    moves.append((piece_x-i-1, piece_y))
        else:
            other_color, _ = board[(piece_x-i-1, piece_y)].split()
            if other_color != piece_color:
                if not check_worry:
                    moves.append((piece_x-i-1, piece_y))
                else:
                    temp_board = board.copy()
                    del temp_board[coords]
                    temp_board[(piece_x-i-1, piece_y)] = move_piece
                    if not is_in_check(piece_color, temp_board):
                        moves.append((piece_x-i-1, piece_y))
            break
    for i in range(7-piece_x):
        if (piece_x+i+1, piece_y) not in board.keys():
            if not check_worry:
                moves.append((piece_x+i+1, piece_y))
            else:
                temp_board = board.copy()
                del temp_board[coords]
                temp_board[(piece_x+i+1, piece_y)] = move_piece
                if not is_in_check(piece_color, temp_board):
                    moves.append((piece_x+i+1, piece_y))
        else:
            other_color, _ = board[(piece_x+i+1, piece_y)].split()
            if other_color != piece_color:
                if not check_worry:
                    moves.append((piece_x+i+1, piece_y))
                else:
                    temp_board = board.copy()
                    del temp_board[coords]
                    temp_board[(piece_x+i+1, piece_y)] = move_piece
                    if not is_in_check(piece_color, temp_board):
                        moves.append((piece_x+i+1, piece_y))
            break
    for i in range(piece_y):
        if (piece_x, piece_y-i-1) not in board.keys():
            if not check_worry:
                moves.append((piece_x, piece_y-i-1))
            else:
                temp_board = board.copy()
                del temp_board[coords]
                temp_board[(piece_x, piece_y-i-1)] = move_piece
                if not is_in_check(piece_color, temp_board):
                    moves.append((piece_x, piece_y-i-1))
        else:
            other_color, _ = board[(piece_x, piece_y-i-1)].split()
            if other_color != piece_color:
                if not check_worry:
                    moves.append((piece_x, piece_y-i-1))
                else:
                    temp_board = board.copy()
                    del temp_board[coords]
                    temp_board[(piece_x, piece_y-i-1)] = move_piece
                    if not is_in_check(piece_color, temp_board):
                        moves.append((piece_x, piece_y-i-1))
            break
    for i in range(7-piece_y):
        if (piece_x, piece_y+i+1) not in board.keys():
            if not check_worry:
                moves.append((piece_x, piece_y+i+1))
            else:
                temp_board = board.copy()
                del temp_board[coords]
                temp_board[(piece_x, piece_y+i+1)] = move_piece
                if not is_in_check(piece_color, temp_board):
                    moves.append((piece_x, piece_y+i+1))
        else:
            other_color, _ = board[(piece_x, piece_y+i+1)].split()
            if other_color != piece_color:
                if not check_worry:
                    moves.append((piece_x, piece_y+i+1))
                else:
                    temp_board = board.copy()
                    del temp_board[coords]
                    temp_board[(piece_x, piece_y+i+1)] = move_piece
                    if not is_in_check(piece_color, temp_board):
                        moves.append((piece_x, piece_y+i+1))
            break
    return moves


def knight_moves(coords, board):
    moves = []
    move_piece = board[coords]
    piece_color, _ = move_piece.split()
    piece_x, piece_y = coords
    temp_board = board.copy()
    del temp_board[coords]
    check_worry = False
    if is_in_check(piece_color, temp_board):
        check_worry = True
    if (piece_x+1, piece_y-2) not in board.keys():
        if not check_worry:
            moves.append((piece_x+1, piece_y-2))
        else:
            temp_board = board.copy()
            del temp_board[coords]
            temp_board[(piece_x+1, piece_y-2)] = move_piece
            if not is_in_check(piece_color, temp_board):
                moves.append((piece_x+1, piece_y-2))
    else:
        other_color, _ = board[(piece_x+1, piece_y-2)].split()
        if other_color != piece_color:
            if not check_worry:
                moves.append((piece_x+1, piece_y-2))
            else:
                temp_board = board.copy()
                del temp_board[coords]
                temp_board[(piece_x+1, piece_y-2)] = move_piece
                if not is_in_check(piece_color, temp_board):
                    moves.append((piece_x+1, piece_y-2))
    if (piece_x+2, piece_y-1) not in board.keys():
        if not check_worry:
            moves.append((piece_x+2, piece_y-1))
        else:
            temp_board = board.copy()
            del temp_board[coords]
            temp_board[(piece_x+2, piece_y-1)] = move_piece
            if not is_in_check(piece_color, temp_board):
                moves.append((piece_x+2, piece_y-1))
    else:
        other_color, _ = board[(piece_x+2, piece_y-1)].split()
        if other_color != piece_color:
            if not check_worry:
                moves.append((piece_x+2, piece_y-1))
            else:
                temp_board = board.copy()
                del temp_board[coords]
                temp_board[(piece_x+2, piece_y-1)] = move_piece
                if not is_in_check(piece_color, temp_board):
                    moves.append((piece_x+2, piece_y-1))
    if (piece_x+2, piece_y+1) not in board.keys():
        if not check_worry:
            moves.append((piece_x+2, piece_y+1))
        else:
            temp_board = board.copy()
            del temp_board[coords]
            temp_board[(piece_x+2, piece_y+1)] = move_piece
            if not is_in_check(piece_color, temp_board):
                moves.append((piece_x+2, piece_y+1))
    else:
        other_color, _ = board[(piece_x+2, piece_y+1)].split()
        if other_color != piece_color:
            if not check_worry:
                moves.append((piece_x+2, piece_y+1))
            else:
                temp_board = board.copy()
                del temp_board[coords]
                temp_board[(piece_x+2, piece_y+1)] = move_piece
                if not is_in_check(piece_color, temp_board):
                    moves.append((piece_x+2, piece_y+1))
    if (piece_x+1, piece_y+2) not in board.keys():
        if not check_worry:
            moves.append((piece_x+1, piece_y+2))
        else:
            temp_board = board.copy()
            del temp_board[coords]
            temp_board[(piece_x+1, piece_y+2)] = move_piece
            if not is_in_check(piece_color, temp_board):
                moves.append((piece_x+1, piece_y+2))
    else:
        other_color, _ = board[(piece_x+1, piece_y+2)].split()
        if other_color != piece_color:
            if not check_worry:
                moves.append((piece_x+1, piece_y+2))
            else:
                temp_board = board.copy()
                del temp_board[coords]
                temp_board[(piece_x+1, piece_y+2)] = move_piece
                if not is_in_check(piece_color, temp_board):
                    moves.append((piece_x+1, piece_y+2))
    if (piece_x-1, piece_y+2) not in board.keys():
        if not check_worry:
            moves.append((piece_x-1, piece_y+2))
        else:
            temp_board = board.copy()
            del temp_board[coords]
            temp_board[(piece_x-1, piece_y+2)] = move_piece
            if not is_in_check(piece_color, temp_board):
                moves.append((piece_x-1, piece_y+2))
    else:
        other_color, _ = board[(piece_x-1, piece_y+2)].split()
        if other_color != piece_color:
            if not check_worry:
                moves.append((piece_x-1, piece_y+2))
            else:
                temp_board = board.copy()
                del temp_board[coords]
                temp_board[(piece_x-1, piece_y+2)] = move_piece
                if not is_in_check(piece_color, temp_board):
                    moves.append((piece_x-1, piece_y+2))
    if (piece_x-2, piece_y+1) not in board.keys():
        if not check_worry:
            moves.append((piece_x-2, piece_y+1))
        else:
            temp_board = board.copy()
            del temp_board[coords]
            temp_board[(piece_x-2, piece_y+1)] = move_piece
            if not is_in_check(piece_color, temp_board):
                moves.append((piece_x-2, piece_y+1))
    else:
        other_color, _ = board[(piece_x-2, piece_y+1)].split()
        if other_color != piece_color:
            if not check_worry:
                moves.append((piece_x-2, piece_y+1))
            else:
                temp_board = board.copy()
                del temp_board[coords]
                temp_board[(piece_x-2, piece_y+1)] = move_piece
                if not is_in_check(piece_color, temp_board):
                    moves.append((piece_x-2, piece_y+1))
    if (piece_x-2, piece_y-1) not in board.keys():
        if not check_worry:
            moves.append((piece_x-2, piece_y-1))
        else:
            temp_board = board.copy()
            del temp_board[coords]
            temp_board[(piece_x-2, piece_y-1)] = move_piece
            if not is_in_check(piece_color, temp_board):
                moves.append((piece_x-2, piece_y-1))
    else:
        other_color, _ = board[(piece_x-2, piece_y-1)].split()
        if other_color != piece_color:
            if not check_worry:
                moves.append((piece_x-2, piece_y-1))
            else:
                temp_board = board.copy()
                del temp_board[coords]
                temp_board[(piece_x-2, piece_y-1)] = move_piece
                if not is_in_check(piece_color, temp_board):
                    moves.append((piece_x-2, piece_y-1))
    if (piece_x-1, piece_y-2) not in board.keys():
        if not check_worry:
            moves.append((piece_x-1, piece_y-2))
        else:
            temp_board = board.copy()
            del temp_board[coords]
            temp_board[(piece_x-1, piece_y-2)] = move_piece
            if not is_in_check(piece_color, temp_board):
                moves.append((piece_x-1, piece_y-2))
    else:
        other_color, _ = board[(piece_x-1, piece_y-2)].split()
        if other_color != piece_color:
            if not check_worry:
                moves.append((piece_x-1, piece_y-2))
            else:
                temp_board = board.copy()
                del temp_board[coords]
                temp_board[(piece_x-1, piece_y-2)] = move_piece
                if not is_in_check(piece_color, temp_board):
                    moves.append((piece_x-1, piece_y-2))
    return moves


def bishop_moves(player, board):
    moves = []
    # TO DO !!!
    return moves


def is_in_check(player, board):
    # find king
    for coords, piece in board.iteritems():
        color, type = piece.split()
        if color == player and type == 'king':
            king_x, king_y = coords
            break
    for i in range(king_y):
        if (king_x, king_y-i-1) in board.keys():
            check_piece = board[(king_x, king_y-i-1)]
            check_color, check_type = check_piece.split()
            if check_color != player and (check_type == 'rook' or check_type == 'queen'):
                return True
            else:
                break
    # check down
    for i in range(7-king_y):
        if (king_x, king_y+i+1) in board.keys():
            check_piece = board[(king_x, king_y+i+1)]
            check_color, check_type = check_piece.split()
            if check_color != player and (check_type == 'rook' or check_type == 'queen'):
                return True
            else:
                break
    # check left
    for i in range(king_x):
        if (king_x-i-1, king_y) in board.keys():
            check_piece = board[(king_x-i-1, king_y)]
            check_color, check_type = check_piece.split()
            if check_color != player and (check_type == 'rook' or check_type == 'queen'):
                return True
            elif check_color == player:
                break
    # check right
    for i in range(7-king_x):
        if (king_x+i+1, king_y) in board.keys():
            check_piece = board[(king_x+i+1, king_y)]
            check_color, check_type = check_piece.split()
            if check_color != player and (check_type == 'rook' or check_type == 'queen'):
                return True
            else:
                break
    # up-left
    for i in range(min(king_x, king_y)):
        if (king_x-i-1, king_y-i-1) in board.keys():
            check_piece = board[(king_x-i-1, king_y-i-1)]
            check_color, check_type = check_piece.split()
            if check_color != player:
                if check_type == 'bishop' or check_type == 'queen':
                    return True
                elif player == 'white' and i == 0 and check_type == 'pawn':
                    return True
                else:
                    break
            else:
                break
    # up-right
    for i in range(min(7-king_x, king_y)):
        if (king_x+i+1, king_y-i-1) in board.keys():
            check_piece = board[(king_x+i+1, king_y-i-1)]
            check_color, check_type = check_piece.split()
            if check_color != player:
                if check_type == 'bishop' or check_type == 'queen':
                    return True
                elif player == 'white' and i == 0 and check_type == 'pawn':
                    return True
                else:
                    break
            else:
                break
    # down-right
    for i in range(min(7-king_x, 7-king_y)):
        if (king_x+i+1, king_y+i+1) in board.keys():
            check_piece = board[(king_x+i+1, king_y+i+1)]
            check_color, check_type = check_piece.split()
            if check_color != player:
                if check_type == 'bishop' or check_type == 'queen':
                    return True
                elif player == 'black' and i == 0 and check_type == 'pawn':
                    return True
                else:
                    break
            else:
                break
    # down-left
    for i in range(min(king_x, 7-king_y)):
        if (king_x-i-1, king_y+i+1) in board.keys():
            check_piece = board[(king_x-i-1, king_y+i+1)]
            check_color, check_type = check_piece.split()
            if check_color != player:
                if check_type == 'bishop' or check_type == 'queen':
                    return True
                elif player == 'black' and i == 0 and check_type == 'pawn':
                    return True
                else:
                    break
            else:
                break
    # knight 1 'o clock
    if (king_x+1, king_y-2) in board.keys():
        check_piece = board[(king_x+1, king_y-2)]
        check_color, check_type = check_piece.split()
        if check_color != player and check_type == 'knight':
            return True
    # knight 2 'o clock
    if (king_x+2, king_y-1) in board.keys():
        check_piece = board[(king_x+2, king_y-1)]
        check_color, check_type = check_piece.split()
        if check_color != player and check_type == 'knight':
            return True
    # knight 4 'o clock
    if (king_x+2, king_y+1) in board.keys():
        check_piece = board[(king_x+2, king_y+1)]
        check_color, check_type = check_piece.split()
        if check_color != player and check_type == 'knight':
            return True
    # knight 5 'o clock
    if (king_x+1, king_y+2) in board.keys():
        check_piece = board[(king_x+1, king_y+2)]
        check_color, check_type = check_piece.split()
        if check_color != player and check_type == 'knight':
            return True
    # knight 7 'o clock
    if (king_x-1, king_y+2) in board.keys():
        check_piece = board[(king_x-1, king_y+2)]
        check_color, check_type = check_piece.split()
        if check_color != player and check_type == 'knight':
            return True
    # knight 8 'o clock
    if (king_x-2, king_y+1) in board.keys():
        check_piece = board[(king_x-2, king_y+1)]
        check_color, check_type = check_piece.split()
        if check_color != player and check_type == 'knight':
            return True
    # knight 10 'o clock
    if (king_x-2, king_y-1) in board.keys():
        check_piece = board[(king_x-2, king_y-1)]
        check_color, check_type = check_piece.split()
        if check_color != player and check_type == 'knight':
            return True
    # knight 11 'o clock
    if (king_x-1, king_y-2) in board.keys():
        check_piece = board[(king_x-1, king_y-2)]
        check_color, check_type = check_piece.split()
        if check_color != player and check_type == 'knight':
            return True
    return False


if __name__ == '__main__':
    main()