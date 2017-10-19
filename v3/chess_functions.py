import copy

COLORS = ['w', 'b']
STARTING_RANKS = {'w': 7, 'b': 0}
MOVE_DIRECTION = {'w': -1, 'b': 1}
OPPOSITE_COLOR = {'w': 'b', 'b': 'w'}


def in_check(color, board, other_coords=None):
    if other_coords is None:
        for check_coords, check_piece in board.iteritems():
            check_color, check_type = check_piece
            if check_color == color and check_type == 'k':
                king_coords = check_coords
                break
    else:
        king_coords = other_coords
    king_x, king_y = king_coords
    for i in range(king_x):
        check_coords = (king_x - i - 1, king_y)
        if check_coords in board.keys():
            check_color, check_type = board[check_coords]
            if check_color == OPPOSITE_COLOR[color] and (check_type in ['r', 'q'] or (i == 0 and check_type == 'k')):
                return True
            break
    for i in range(7 - king_x):
        check_coords = (king_x + i + 1, king_y)
        if check_coords in board.keys():
            check_color, check_type = board[check_coords]
            if check_color == OPPOSITE_COLOR[color] and (check_type in ['r', 'q'] or (i == 0 and check_type == 'k')):
                return True
            break
    for i in range(king_y):
        check_coords = (king_x, king_y - i - 1)
        if check_coords in board.keys():
            check_color, check_type = board[check_coords]
            if check_color == OPPOSITE_COLOR[color] and (check_type in ['r', 'q'] or (i == 0 and check_type == 'k')):
                return True
            break
    for i in range(7 - king_y):
        check_coords = (king_x, king_y + i + 1)
        if check_coords in board.keys():
            check_color, check_type = board[check_coords]
            if check_color == OPPOSITE_COLOR[color] and (check_type in ['r', 'q'] or (i == 0 and check_type == 'k')):
                return True
            break
    for i in range(min(king_x, king_y)):
        check_coords = (king_x - i - 1, king_y - i - 1)
        if check_coords in board.keys():
            check_color, check_type = board[check_coords]
            if check_color == OPPOSITE_COLOR[color] and (check_type in ['b', 'q'] or (i == 0 and check_type in ['p', 'k'])):
                return True
            break
    for i in range(min(7 - king_x, king_y)):
        check_coords = (king_x + i + 1, king_y - i - 1)
        if check_coords in board.keys():
            check_color, check_type = board[check_coords]
            if check_color == OPPOSITE_COLOR[color] and (check_type in ['b', 'q'] or (i == 0 and check_type in ['p', 'k'])):
                return True
            break
    for i in range(min(7 - king_x, 7 - king_y)):
        check_coords = (king_x + i + 1, king_y + i + 1)
        if check_coords in board.keys():
            check_color, check_type = board[check_coords]
            if check_color == OPPOSITE_COLOR[color] and (check_type in ['b', 'q'] or (i == 0 and check_type in ['p', 'k'])):
                return True
            break
    for i in range(min(king_x, 7 - king_y)):
        check_coords = (king_x - i - 1, king_y + i + 1)
        if check_coords in board.keys():
            check_color, check_type = board[check_coords]
            if check_color == OPPOSITE_COLOR[color] and (check_type in ['b', 'q'] or (i == 0 and check_type in ['p', 'k'])):
                return True
            break
    knight_pattern = [(king_x - 2, king_y - 1), (king_x - 1, king_y - 2),
                    (king_x + 1, king_y - 2), (king_x + 2, king_y - 1),
                    (king_x + 2, king_y + 1), (king_x + 1, king_y + 2),
                    (king_x - 1, king_y + 2), (king_x - 2, king_y + 1)]
    for check_coords in knight_pattern:
        if check_coords in board.keys():
            check_color, check_type = board[check_coords]
            if check_color == OPPOSITE_COLOR[color] and check_type == 'n':
                return True
    return False


def pawn_moves(coords, board, pawn_jump_file):
    moves = []
    if pawn_jump_file is None:
        pawn_jump_file = 99
    for check_coords, check_piece in board.iteritems():
        if coords == check_coords:
            check_color, check_type = check_piece
            break
    # forward
    if (coords[0], coords[1] + MOVE_DIRECTION[check_color]) not in board.keys():
        moves.append((coords[0], coords[1] + MOVE_DIRECTION[check_color]))
        if coords[1] == STARTING_RANKS[check_color] + MOVE_DIRECTION[check_color] and (coords[0], coords[1] + 2 * MOVE_DIRECTION[check_color]) not in board.keys():
            moves.append((coords[0], coords[1] + 2 * MOVE_DIRECTION[check_color]))
    # e.p. left
    if coords[0] - 1 == pawn_jump_file and coords[1] == STARTING_RANKS[check_color] + 4 * MOVE_DIRECTION[check_color]:
        moves.append((coords[0] - 1, coords[1] + MOVE_DIRECTION[check_color]))
    # attack left
    elif (coords[0] - 1, coords[1] + MOVE_DIRECTION[check_color]) in board.keys():
        attack_color, _ = board[(coords[0] - 1, coords[1] + MOVE_DIRECTION[check_color])]
        if attack_color == OPPOSITE_COLOR[check_color]:
            moves.append((coords[0] - 1, coords[1] + MOVE_DIRECTION[check_color]))
    # e.p. right
    if coords[0] + 1 == pawn_jump_file and coords[1] == STARTING_RANKS[check_color] + 4 * MOVE_DIRECTION[check_color]:
        moves.append((coords[0] + 1, coords[1] + MOVE_DIRECTION[check_color]))
    # attack right
    elif (coords[0] + 1, coords[1] + MOVE_DIRECTION[check_color]) in board.keys():
        attack_color, _ = board[(coords[0] + 1, coords[1] + MOVE_DIRECTION[check_color])]
        if attack_color == OPPOSITE_COLOR[check_color]:
            moves.append((coords[0] + 1, coords[1] + MOVE_DIRECTION[check_color]))
    return moves


def orthogonal_moves(coords, board):
    piece_color, _ = board[coords]
    x, y = coords
    moves = []
    for i in range(x):
        check_coords = (x - i - 1, y)
        if check_coords not in board.keys():
            moves.append(check_coords)
        else:
            check_color, _ = board[check_coords]
            if check_color == OPPOSITE_COLOR[piece_color]:
                moves.append(check_coords)
            break
    for i in range(7 - x):
        check_coords = (x + i + 1, y)
        if check_coords not in board.keys():
            moves.append(check_coords)
        else:
            check_color, _ = board[check_coords]
            if check_color == OPPOSITE_COLOR[piece_color]:
                moves.append(check_coords)
            break
    for i in range(y):
        check_coords = (x, y - i - 1)
        if check_coords not in board.keys():
            moves.append(check_coords)
        else:
            check_color, _ = board[check_coords]
            if check_color == OPPOSITE_COLOR[piece_color]:
                moves.append(check_coords)
            break
    for i in range(7 - y):
        check_coords = (x, y + i + 1)
        if check_coords not in board.keys():
            moves.append(check_coords)
        else:
            check_color, _ = board[check_coords]
            if check_color == OPPOSITE_COLOR[piece_color]:
                moves.append(check_coords)
            break
    return moves


def diagonal_moves(coords, board):
    piece_color, _ = board[coords]
    x, y = coords
    moves = []
    for i in range(min(x, y)):
        check_coords = (x - i - 1, y - i - 1)
        if check_coords not in board.keys():
            moves.append(check_coords)
        else:
            check_color, _ = board[check_coords]
            if check_color == OPPOSITE_COLOR[piece_color]:
                moves.append(check_coords)
            break
    for i in range(min(7 - x, y)):
        check_coords = (x + i + 1, y - i - 1)
        if check_coords not in board.keys():
            moves.append(check_coords)
        else:
            check_color, _ = board[check_coords]
            if check_color == OPPOSITE_COLOR[piece_color]:
                moves.append(check_coords)
            break
    for i in range(min(7 - x, 7 - y)):
        check_coords = (x + i + 1, y + i + 1)
        if check_coords not in board.keys():
            moves.append(check_coords)
        else:
            check_color, _ = board[check_coords]
            if check_color == OPPOSITE_COLOR[piece_color]:
                moves.append(check_coords)
            break
    for i in range(min(x, 7 - y)):
        check_coords = (x - i - 1, y + i + 1)
        if check_coords not in board.keys():
            moves.append(check_coords)
        else:
            check_color, _ = board[check_coords]
            if check_color == OPPOSITE_COLOR[piece_color]:
                moves.append(check_coords)
            break
    return moves


def knight_moves(coords, board):
    x, y = coords
    piece_color, _ = board[coords]
    move_pattern = [(x - 2, y - 1), (x - 1, y - 2),
                    (x + 1, y - 2), (x + 2, y - 1),
                    (x + 2, y + 1), (x + 1, y + 2),
                    (x - 1, y + 2), (x - 2, y + 1)]
    moves = []
    for move in move_pattern:
        if move not in board.keys():
            moves.append(move)
        else:
            check_color, _ = board[move]
            if check_color == OPPOSITE_COLOR[piece_color]:
                moves.append(move)
    return moves


def king_moves(coords, board, castle_flags):
    x, y = coords
    piece_color, _ = board[coords]
    moves = []
    move_pattern = [(x - 1, y - 1), (x, y - 1),
                    (x + 1, y - 1), (x + 1, y),
                    (x + 1, y + 1), (x, y + 1),
                    (x - 1, y + 1), (x - 1, y)]
    for move in move_pattern:
        if move not in board.keys():
            moves.append(move)
        else:
            check_color, _ = board[move]
            if check_color == OPPOSITE_COLOR[piece_color]:
                moves.append(move)
    if not castle_flags['king_moved']:
        # left castle
        if not castle_flags['queen_rook_moved']:
            queen_castle = True
            for x in range(1, 4):
                if (x, STARTING_RANKS[piece_color]) in board.keys() or in_check(piece_color, board, other_coords=(x, STARTING_RANKS[piece_color])):
                    queen_castle = False
                    break
            if queen_castle:
                moves.append((2, STARTING_RANKS[piece_color]))
        # right castle
        if not castle_flags['king_rook_moved']:
            king_castle = True
            for x in range(5, 7):
                if (x, STARTING_RANKS[piece_color]) in board.keys() or in_check(piece_color, board, other_coords=(x, STARTING_RANKS[piece_color])):
                    king_castle = False
                    break
            if king_castle:
                moves.append((6, STARTING_RANKS[piece_color]))
    return moves


def moves_available(coords, board, castle_flags, pawn_jump=None):
    moves = []
    check_color, check_type = board[coords]
    if check_type == 'p':
        moves.extend(pawn_moves(coords, board, pawn_jump))
    if check_type in ['r', 'q']:
        moves.extend(orthogonal_moves(coords, board))
    if check_type in ['b', 'q']:
        moves.extend(diagonal_moves(coords, board))
    if check_type == 'n':
        moves.extend(knight_moves(coords, board))
    if check_type == 'k':
        moves.extend(king_moves(coords, board, castle_flags))
    moves = list(set(moves))
    valid_moves = []
    for move in moves:
        if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
            check_board = copy.deepcopy(board)
            check_board[move] = check_board.pop(coords)
            if not in_check(check_color, check_board):
                valid_moves.append(move)
    return valid_moves


def make_move(from_coords, to_coords, board):
    if to_coords in board.keys():
        taken_piece = board[to_coords]
    else:
        taken_piece = None
    board[to_coords] = board.pop(from_coords)
    return taken_piece


def generate_starting_board():
    board = {}
    for color in COLORS:
        for x in range(8):
            board[(x, STARTING_RANKS[color] + MOVE_DIRECTION[color])] = (color, 'p')
        for i in range(2):
            board[(i * 7, STARTING_RANKS[color])] = (color, 'r')
            board[(i * 5 + 1, STARTING_RANKS[color])] = (color, 'n')
            board[(i * 3 + 2, STARTING_RANKS[color])] = (color, 'b')
        board[(3, STARTING_RANKS[color])] = (color, 'q')
        board[(4, STARTING_RANKS[color])] = (color, 'k')
    return board
