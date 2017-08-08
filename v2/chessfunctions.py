import copy


def convert_coords_to_notation(tile_coords):
    file_str = 'abcdefgh'
    x = file_str[tile_coords[0]]
    y = 8 - tile_coords[1]
    return '{}{}'.format(x, y)


def convert_notation_to_coords(tile_notation):
    file_dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    assert len(tile_notation) == 2, 'convert: invalid tile notation: len != 2'
    assert tile_notation[0].lower() in file_dict.keys()
    assert 1 <= int(tile_notation[1]) <= 8
    x = file_dict[tile_notation[0].lower()]
    y = 8 - int(tile_notation[1])
    return (x, y)


def generate_new_pieces():
    pieces = {}
    for x in range(8):
        pieces[(x, 1)] = 'bp'
        pieces[(x, 6)] = 'wp'
    pieces[(0, 0)] = 'br'
    pieces[(7, 0)] = 'br'
    pieces[(1, 0)] = 'bn'
    pieces[(6, 0)] = 'bn'
    pieces[(2, 0)] = 'bb'
    pieces[(5, 0)] = 'bb'
    pieces[(3, 0)] = 'bq'
    pieces[(4, 0)] = 'bk'
    pieces[(0, 7)] = 'wr'
    pieces[(7, 7)] = 'wr'
    pieces[(1, 7)] = 'wn'
    pieces[(6, 7)] = 'wn'
    pieces[(2, 7)] = 'wb'
    pieces[(5, 7)] = 'wb'
    pieces[(3, 7)] = 'wq'
    pieces[(4, 7)] = 'wk'
    return pieces


def in_check(check_color, piece_dict):
    assert check_color in ['b', 'w'], 'in_check: invalid color passed.'
    king_coords = None
    for coords, piece in piece_dict.iteritems():
        if piece[0] == check_color and piece[1] == 'k':
            king_coords = coords
    assert king_coords is not None, 'in_check: {} king not found.'.format(check_color)
    orthog = return_orthogonal_moves(king_coords, piece_dict)
    for space in orthog:
        if space in piece_dict.keys():
            if piece_dict[space][0] != check_color:
                if piece_dict[space][1] == 'r' or piece_dict[space][1] == 'q':
                    return True
                elif piece_dict[space][1] == 'k':
                    if king_coords[0] == space[0] and \
                            (king_coords[1] - space[1] == 1 or king_coords[1] - space[1] == -1):
                        return True
                    elif king_coords[1] == space[1] and \
                            (king_coords[0] - space[0] == 1 or king_coords[0] - space[0] == -1):
                        return True
    diag = return_diagonal_moves(king_coords, piece_dict)
    for space in diag:
        if space in piece_dict.keys():
            if piece_dict[space][0] != check_color:
                if piece_dict[space][1] == 'b' or piece_dict[space][1] == 'q':
                    return True
                elif piece_dict[space][1] == 'p':
                    if check_color == 'w' and king_coords[1] - space[1] == 1:
                        return True
                    elif check_color == 'b' and king_coords[1] - space[1] == -1:
                        return True
                elif piece_dict[space][1] == 'k':
                    if (king_coords[0] - space[0] == 1 or king_coords[0] - space[0] == -1) and \
                            (king_coords[1] - space[1] == 1 or king_coords[1] - space[1] == -1):
                        return True
    knig = return_knight_moves(king_coords, piece_dict)
    for space in knig:
        if space in piece_dict.keys():
            if piece_dict[space][0] != check_color:
                if piece_dict[space][1] == 'n':
                    return True
    return False


def no_available_moves(move_color, piece_dict):
    #TODO -- needs testing
    for coords, piece in piece_dict.iteritems():
        if piece[0] == move_color:
            moves = return_moves(coords, piece_dict)
            if len(moves) > 0:
                return False
    return True


def move_piece(from_coords, to_coords, piece_dict):
    assert from_coords in piece_dict.keys(), 'move_piece: piece not found to move at {}'.format(from_coords)
    assert min(to_coords) >= 0 and max(to_coords) <= 7, 'move_piece: invalid coords to move to: {}'.format(to_coords)
    piece_dict[to_coords] = piece_dict.pop(from_coords)


def return_moves(move_coords, piece_dict):
    assert move_coords in piece_dict.keys(), 'return_moves: no piece found at {}'.format(move_coords)
    move_color = piece_dict[move_coords][0]
    move_piece = piece_dict[move_coords][1]
    moves = []
    assert move_color in ['b', 'w'], 'return_moves: invalid piece at {}: {}'.format(move_coords, piece_dict[move_coords])
    assert move_piece in ['p', 'r', 'n', 'b', 'q', 'k'], 'return_moves: invalid piece at {}: {}'.format(move_coords, piece_dict[move_coords])
    if move_piece == 'p':
        moves = return_pawn_moves(move_coords, piece_dict)
    elif move_piece  == 'r':
        moves = return_orthogonal_moves(move_coords, piece_dict)
    elif move_piece == 'n':
        moves = return_knight_moves(move_coords, piece_dict)
    elif move_piece == 'b':
        moves = return_diagonal_moves(move_coords, piece_dict)
    elif move_piece == 'q':
        moves = return_orthogonal_moves(move_coords, piece_dict)
        moves.extend(return_diagonal_moves(move_coords, piece_dict))
    elif move_piece == 'k':
        moves = return_king_moves(move_coords, piece_dict)
    moves = list(set(moves))
    valid_moves = []
    for possible_move in moves:
        pieces_copy = copy.deepcopy(piece_dict)
        pieces_copy[possible_move] = pieces_copy.pop(move_coords)
        if not in_check(move_color, pieces_copy):
            valid_moves.append(possible_move)
    return valid_moves


def return_orthogonal_moves(move_coords, piece_dict):
    move_color = piece_dict[move_coords][0]
    x, y = move_coords
    moves = []
    for i in range(1, 8-x):
        possible_move = (x+i, y)
        if possible_move in piece_dict.keys():
            if move_color != piece_dict[possible_move][0]:
                moves.append(possible_move)
            break
        moves.append(possible_move)
    for i in range(1, x+1):
        possible_move = (x-i, y)
        if possible_move in piece_dict.keys():
            if move_color != piece_dict[possible_move][0]:
                moves.append(possible_move)
            break
        moves.append(possible_move)
    for i in range(1, 8-y):
        possible_move = (x, y+i)
        if possible_move in piece_dict.keys():
            if move_color != piece_dict[possible_move][0]:
                moves.append(possible_move)
            break
        moves.append(possible_move)
    for i in range(1, y+1):
        possible_move = (x, y-i)
        if possible_move in piece_dict.keys():
            if move_color != piece_dict[possible_move][0]:
                moves.append(possible_move)
            break
        moves.append(possible_move)
    return moves


def return_diagonal_moves(move_coords, piece_dict):
    move_color = piece_dict[move_coords][0]
    x, y = move_coords
    moves = []
    for i in range(1, min(x, y) + 1):
        possible_move = (x - i, y - i)
        if possible_move in piece_dict.keys():
            if move_color != piece_dict[possible_move][0]:
                moves.append(possible_move)
            break
        moves.append(possible_move)
    for i in range(1, min(7 - x, y) + 1):
        possible_move = (x + i, y - i)
        if possible_move in piece_dict.keys():
            if move_color != piece_dict[possible_move][0]:
                moves.append(possible_move)
            break
        moves.append(possible_move)
    for i in range(1, min(8 - x, 8 - y)):
        possible_move = (x + i, y + i)
        if possible_move in piece_dict.keys():
            if move_color != piece_dict[possible_move][0]:
                moves.append(possible_move)
            break
        moves.append(possible_move)
    for i in range(1, min(x, 7 - y) + 1):
        possible_move = (x - i, y + i)
        if possible_move in piece_dict.keys():
            if move_color != piece_dict[possible_move][0]:
                moves.append(possible_move)
            break
        moves.append(possible_move)
    return moves


def return_knight_moves(move_coords, piece_dict):
    move_color = piece_dict[move_coords][0]
    x, y = move_coords
    moves = []
    knight_moves = [(x - 2, y - 1), (x - 1, y - 2), (x + 1, y - 2), (x + 2, y - 1),
                    (x + 2, y + 1), (x + 1, y + 2), (x - 1, y + 2), (x - 2, y + 1)]
    for possible_move in knight_moves:
        if min(possible_move) >= 0 and max(possible_move) <= 7:
            if possible_move in piece_dict.keys():
                if move_color != piece_dict[possible_move][0]:
                    moves.append(possible_move)
            else:
                moves.append(possible_move)
    return moves


def return_pawn_moves(move_coords, piece_dict):
    move_color = piece_dict[move_coords][0]
    x, y = move_coords
    moves = []
    if move_color == 'w':
        move_dir = -1
    elif move_color == 'b':
        move_dir = 1
    possible_move = (x, y + move_dir)
    if possible_move not in piece_dict.keys():
        moves.append(possible_move)
        if (move_color == 'w' and y == 6) or (move_color == 'b' and y == 1):
            possible_move = (x, y + 2 * move_dir)
            if possible_move not in piece_dict.keys():
                moves.append(possible_move)
    possible_move = (x - 1, y + move_dir)
    if possible_move in piece_dict.keys():
        if move_color != piece_dict[possible_move][0]:
            moves.append(possible_move)
    possible_move = (x + 1, y + move_dir)
    if possible_move in piece_dict.keys():
        if move_color != piece_dict[possible_move][0]:
            moves.append(possible_move)
    return moves


def return_king_moves(move_coords, piece_dict):
    move_color = piece_dict[move_coords][0]
    x, y = move_coords
    moves = []
    king_moves = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x + 1, y),
                  (x + 1, y + 1), (x, y + 1), (x - 1, y + 1), (x - 1, y)]
    for possible_move in king_moves:
        if min(possible_move) >= 0 and max(possible_move) <= 7:
            if possible_move in piece_dict.keys():
                if move_color != piece_dict[possible_move][0]:
                    moves.append(possible_move)
            else:
                moves.append(possible_move)
    return moves
