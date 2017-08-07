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


def in_check(color, pieces_dict):
    assert color[0] in ['b', 'w'], 'in_check: Invalid color given.'
    king_coords = None
    for coords, piece in pieces_dict.iteritems():
        if piece == '{}k'.format(color[0]):
            king_coords = coords
            break
    assert king_coords is not None, 'in_check: {} king not found.'.format(color[0])
    _, diag_enemies = return_diagonals(king_coords, pieces_dict)
    for enemy in diag_enemies:
        if pieces_dict[enemy][1] == 'b' or pieces_dict[enemy][1] == 'q':
            return True
        elif pieces_dict[enemy][1] == 'k':
            if (-1 <= (enemy[0] - king_coords[0]) <= 1) and (-1 <= (enemy[1] - king_coords[1]) <= 1):
                return True
        elif pieces_dict[enemy][1] == 'p':
            if enemy[0] == king_coords[0] + 1 or enemy[0] == king_coords[0] - 1:
                if (color[0] == 'w' and enemy[1] == king_coords[1] + 1) or (color[0] == 'b' and enemy[1] == king_coords[1] - 1):
                    return True
    _, ortho_enemies = return_orthogonals(king_coords, pieces_dict)
    for enemy in ortho_enemies:
        if pieces_dict[enemy][1] == 'r' or pieces_dict[enemy][1] == 'q':
            return True
        elif pieces_dict[enemy][1] == 'k':
            if (-1 <= (enemy[0] - king_coords[0]) <= 1) and (-1 <= (enemy[1] - king_coords[1]) <= 1):
                return True
    _, knight_enemies = return_knights(king_coords, pieces_dict)
    for enemy in knight_enemies:
        if pieces_dict[enemy][1] == 'n':
            return True
    return False


def return_diagonals(coords, pieces_dict):
    """
    Given the coordinates of a piece to move, return free spaces and any enemies which stop movement.

    coords: (int x, int y) - where x and y represent the position with 0 <= x, y <= 7
    pieces_dict: { coords position: str piece_name } - where the piece names are two letters, beginning with either
                                                       'b' for black or 'w' for white and ending with one of:
                                                       'p' for pawn, 'r' for rook, 'n' for knight, 'b' for bishop,
                                                       'q' for queen, or 'k' for king.
    """
    assert 0 <= coords[0] <= 7, 'return_diagonals: Invalid coordinate(s) passed: x'
    assert 0 <= coords[1] <= 7, 'return_diagonals: Invalid coordinate(s) passed: y'
    assert coords in pieces_dict.keys(), 'return_diagonals: No piece to move at {}'.format(coords)
    assert pieces_dict[coords][0] in ['b', 'w'], 'return_diagonals: Invalid piece color at {}'.format(coords)
    free_spaces = []
    enemy_blocks = []
    up_right_spaces, up_right_block = return_diagonals_up_right(coords, pieces_dict)
    free_spaces.extend(up_right_spaces)
    if up_right_block is not None:
        enemy_blocks.append(up_right_block)
    down_right_spaces, down_right_block = return_diagonals_down_right(coords, pieces_dict)
    free_spaces.extend(down_right_spaces)
    if down_right_block is not None:
        enemy_blocks.append(down_right_block)
    down_left_spaces, down_left_block = return_diagonals_down_left(coords, pieces_dict)
    free_spaces.extend(down_left_spaces)
    if down_left_block is not None:
        enemy_blocks.append(down_left_block)
    up_left_spaces, up_left_block = return_diagonals_up_left(coords, pieces_dict)
    free_spaces.extend(up_left_spaces)
    if up_left_block is not None:
        enemy_blocks.append(up_left_block)
    return free_spaces, enemy_blocks


def return_diagonals_up_right(coords, pieces_dict):
    free_spaces = []
    enemy_block = None
    x, y = coords
    color = pieces_dict[coords][0]
    for i in range(min(7-x, y)):
        possible_move = (x+1, y-1)
        if possible_move in pieces_dict.keys():
            if pieces_dict[possible_move][0] != color:
                enemy_block = possible_move
            break
        free_spaces.append(possible_move)
    return free_spaces, enemy_block


def return_diagonals_down_right(coords, pieces_dict):
    free_spaces = []
    enemy_block = None
    x, y = coords
    color = pieces_dict[coords][0]
    for i in range(min(7-x, 7-y)):
        possible_move = (x+1, y+1)
        if possible_move in pieces_dict.keys():
            if pieces_dict[possible_move][0] != color:
                enemy_block = possible_move
            break
        free_spaces.append(possible_move)
    return free_spaces, enemy_block


def return_diagonals_down_left(coords, pieces_dict):
    free_spaces = []
    enemy_block = None
    x, y = coords
    color = pieces_dict[coords][0]
    for i in range(min(x, 7-y)):
        possible_move = (x-1, y+1)
        if possible_move in pieces_dict.keys():
            if pieces_dict[possible_move][0] != color:
                enemy_block = possible_move
            break
        free_spaces.append(possible_move)
    return free_spaces, enemy_block


def return_diagonals_up_left(coords, pieces_dict):
    free_spaces = []
    enemy_block = None
    x, y = coords
    color = pieces_dict[coords][0]
    for i in range(min(x, y)):
        possible_move = (x-1, y-1)
        if possible_move in pieces_dict.keys():
            if pieces_dict[possible_move][0] != color:
                enemy_block = possible_move
            break
        free_spaces.append(possible_move)
    return free_spaces, enemy_block


def return_knights(coords, pieces_dict):
    """
    Given the coordinates of a piece to move, return free spaces and any enemies which stop movement.

    coords: (int x, int y) - where x and y represent the position with 0 <= x, y <= 7
    pieces_dict: { coords position: str piece_name } - where the piece names are two letters, beginning with either
                                                       'b' for black or 'w' for white and ending with one of:
                                                       'p' for pawn, 'r' for rook, 'n' for knight, 'b' for bishop,
                                                       'q' for queen, or 'k' for king.
    """
    assert 0 <= coords[0] <= 7, 'return_knights: Invalid coordinate(s) passed: x'
    assert 0 <= coords[1] <= 7, 'return_knights: Invalid coordinate(s) passed: y'
    assert coords in pieces_dict.keys(), 'return_knights: No piece to move at {}'.format(coords)
    assert pieces_dict[coords][0] in ['b', 'w'], 'return_knights: Invalid piece color at {}'.format(coords)
    free_spaces = []
    enemy_blocks = []
    x, y = coords
    color = pieces_dict[coords][0]
    knight_moves = [(x + 1, y - 2), (x + 2, y - 1), (x + 2, y + 1), (x + 1, y + 2), (x - 1, y + 2), (x - 2, y + 1),
                    (x - 2, y - 1), (x - 1, y - 2)]
    for possible_move in knight_moves:
        if possible_move in pieces_dict:
            if pieces_dict[possible_move][0] != color:
                enemy_blocks.append(possible_move)
        else:
            free_spaces.append(possible_move)
    return free_spaces, enemy_blocks


def return_orthogonals(coords, pieces_dict):
    """
    Given the coordinates of a piece to move, return free spaces and any enemies which stop movement.

    coords: (int x, int y) - where x and y represent the position with 0 <= x, y <= 7
    pieces_dict: { coords position: str piece_name } - where the piece names are two letters, beginning with either
                                                       'b' for black or 'w' for white and ending with one of:
                                                       'p' for pawn, 'r' for rook, 'n' for knight, 'b' for bishop,
                                                       'q' for queen, or 'k' for king.
    """
    assert 0 <= coords[0] <= 7, 'return_diagonals: Invalid coordinate(s) passed: x'
    assert 0 <= coords[1] <= 7, 'return_diagonals: Invalid coordinate(s) passed: y'
    assert coords in pieces_dict.keys(), 'return_diagonals: No piece to move at {}'.format(coords)
    assert pieces_dict[coords][0] in ['b', 'w'], 'return_diagonals: Invalid piece color at {}'.format(coords)
    free_spaces = []
    enemy_blocks = []
    up_spaces, up_block = return_orthogonals_up(coords, pieces_dict)
    free_spaces.extend(up_spaces)
    if up_block is not None:
        enemy_blocks.append(up_block)
    right_spaces, right_block = return_orthogonals_right(coords, pieces_dict)
    free_spaces.extend(right_spaces)
    if right_block is not None:
        enemy_blocks.append(right_block)
    down_spaces, down_block = return_orthogonals_down(coords, pieces_dict)
    free_spaces.extend(down_spaces)
    if down_block is not None:
        enemy_blocks.append(down_block)
    left_spaces, left_block = return_orthogonals_left(coords, pieces_dict)
    free_spaces.extend(left_spaces)
    if left_block is not None:
        enemy_blocks.append(left_block)
    return free_spaces, enemy_blocks


def return_orthogonals_right(coords, pieces_dict):
    free_spaces = []
    enemy_block = None
    x, y = coords
    color = pieces_dict[coords][0]
    for i in range(7 - x):
        possible_move = (x + 1, y)
        if possible_move in pieces_dict.keys():
            if pieces_dict[possible_move][0] != color:
                enemy_block = possible_move
            break
        free_spaces.append(possible_move)
    return free_spaces, enemy_block


def return_orthogonals_down(coords, pieces_dict):
    free_spaces = []
    enemy_block = None
    x, y = coords
    color = pieces_dict[coords][0]
    for i in range(7 - y):
        possible_move = (x, y + 1)
        if possible_move in pieces_dict.keys():
            if pieces_dict[possible_move][0] != color:
                enemy_block = possible_move
            break
        free_spaces.append(possible_move)
    return free_spaces, enemy_block


def return_orthogonals_left(coords, pieces_dict):
    free_spaces = []
    enemy_block = None
    x, y = coords
    color = pieces_dict[coords][0]
    for i in range(x):
        possible_move = (x - 1, y)
        if possible_move in pieces_dict.keys():
            if pieces_dict[possible_move][0] != color:
                enemy_block = possible_move
            break
        free_spaces.append(possible_move)
    return free_spaces, enemy_block


def return_orthogonals_up(coords, pieces_dict):
    free_spaces = []
    enemy_block = None
    x, y = coords
    color = pieces_dict[coords][0]
    for i in range(y):
        possible_move = (x, y - 1)
        if possible_move in pieces_dict.keys():
            if pieces_dict[possible_move][0] != color:
                enemy_block = possible_move
            break
        free_spaces.append(possible_move)
    return free_spaces, enemy_block


def return_valid_attacks(coords, pieces_dict):
    assert coords in pieces_dict.keys(), 'return_valid_attacks: No piece to move found at {}'.format(coords)
    assert pieces_dict[coords][1] in ['p', 'r', 'n', 'b', 'q',
                                      'k'], 'return_valid_attacks: Invalid piece type at {}'.format(coords)
    possible_attacks = []
    if pieces_dict[coords][1] == 'p':
        possible_attacks.extend(return_pawn_attacks(coords, pieces_dict))
    elif pieces_dict[coords][1] == 'r':
        possible_attacks.extend(return_rook_attacks(coords, pieces_dict))
    elif pieces_dict[coords][1] == 'n':
        possible_attacks.extend(return_knight_attacks(coords, pieces_dict))
    elif pieces_dict[coords][1] == 'b':
        possible_attacks.extend(return_bishop_attacks(coords, pieces_dict))
    elif pieces_dict[coords][1] == 'q':
        possible_attacks.extend(return_queen_attacks(coords, pieces_dict))
    elif pieces_dict[coords][1] == 'k':
        possible_attacks.extend(return_king_attacks(coords, pieces_dict))
    attacks = [x for x in possible_attacks if validate_move(coords, x, pieces_dict)]
    return list(set(attacks))


def return_valid_moves(coords, pieces_dict):
    assert coords in pieces_dict.keys(), 'return_valid_moves: No piece to move found at {}'.format(coords)
    assert pieces_dict[coords][1] in ['p', 'r', 'n', 'b', 'q',
                                      'k'], 'return_valid_moves: Invalid piece type at {}'.format(coords)
    possible_moves = []
    if pieces_dict[coords][1] == 'p':
        possible_moves.extend(return_pawn_moves(coords, pieces_dict))
    elif pieces_dict[coords][1] == 'r':
        possible_moves.extend(return_rook_moves(coords, pieces_dict))
    elif pieces_dict[coords][1] == 'n':
        possible_moves.extend(return_knight_moves(coords, pieces_dict))
    elif pieces_dict[coords][1] == 'b':
        possible_moves.extend(return_bishop_moves(coords, pieces_dict))
    elif pieces_dict[coords][1] == 'q':
        possible_moves.extend(return_queen_moves(coords, pieces_dict))
    elif pieces_dict[coords][1] == 'k':
        possible_moves.extend(return_king_moves(coords, pieces_dict))
    moves = [x for x in possible_moves if validate_move(coords, x, pieces_dict)]
    return list(set(moves))


def return_pawn_attacks(coords, pieces_dict):
    attacks = []
    x, y = coords
    if pieces_dict[coords][0] == 'w':
        move_dir = -1
    elif pieces_dict[coords][0] == 'b':
        move_dir = 1
    if (x - 1, y + move_dir) in pieces_dict.keys():
        if pieces_dict[(x - 1, y + move_dir)][0] != pieces_dict[coords][0]:
            attacks.append((x - 1, y + move_dir))
    if (x + 1, y + move_dir) in pieces_dict.keys():
        if pieces_dict[(x + 1, y + move_dir)][0] != pieces_dict[coords][0]:
            attacks.append((x + 1, y + move_dir))
    return attacks


def return_pawn_moves(coords, pieces_dict):
    free_spaces = []
    x, y = coords
    if pieces_dict[coords][0] == 'w':
        move_dir = -1
    elif pieces_dict[coords][0] == 'b':
        move_dir = 1
    if (x, y + move_dir) not in pieces_dict.keys():
        free_spaces.append((x, y + move_dir))
        if 0 <= (y + 2 * move_dir) <= 8 and (x, y + 2 * move_dir) not in pieces_dict.keys():
            free_spaces.append((x, y + 2 * move_dir))
    return free_spaces


def return_rook_attacks(coords, pieces_dict):
    _, attacks = return_orthogonals(coords, pieces_dict)
    return attacks


def return_rook_moves(coords, pieces_dict):
    moves, _ = return_orthogonals(coords, pieces_dict)
    return moves


def return_knight_attacks(coords, pieces_dict):
    _, attacks = return_knights(coords, pieces_dict)
    return attacks


def return_knight_moves(coords, pieces_dict):
    moves, _ = return_knights(coords, pieces_dict)
    return moves


def return_bishop_attacks(coords, pieces_dict):
    _, attacks = return_diagonals(coords, pieces_dict)
    return attacks


def return_bishop_moves(coords, pieces_dict):
    moves, _ = return_diagonals(coords, pieces_dict)
    return moves


def return_queen_attacks(coords, pieces_dict):
    _, diag_attacks = return_diagonals(coords, pieces_dict)
    _, ortho_attacks = return_orthogonals(coords, pieces_dict)
    return diag_attacks + ortho_attacks


def return_queen_moves(coords, pieces_dict):
    diag_moves, _ = return_diagonals(coords, pieces_dict)
    ortho_moves, _ = return_orthogonals(coords, pieces_dict)
    return diag_moves + ortho_moves


def return_king_attacks(coords, pieces_dict):
    _, diag_attacks = return_diagonals(coords, pieces_dict)
    _, ortho_attacks = return_orthogonals(coords, pieces_dict)
    possible_attacks = diag_attacks + ortho_attacks
    attacks = [x for x in possible_attacks if ((-1 <= x[0] - coords[0] <= 1) and (-1 <= x[1] - coords[1] <= 1))]
    return attacks


def return_king_moves(coords, pieces_dict):
    diag_moves, _ = return_diagonals(coords, pieces_dict)
    ortho_moves, _ = return_orthogonals(coords, pieces_dict)
    possible_moves = diag_moves + ortho_moves
    moves = [x for x in possible_moves if ((-1 <= x[0] - coords[0] <= 1) and (-1 <= x[1] - coords[1] <= 1))]
    return moves


def validate_move(from_coords, to_coords, pieces_dict):
    assert from_coords in pieces_dict.keys(), 'validate_move: Piece to move not found at: {}'.format(from_coords)
    move_color = pieces_dict[from_coords][0]
    board_copy = dict((k, v) for k, v in pieces_dict.items())
    board_copy[to_coords] = pieces_dict[from_coords]
    del board_copy[from_coords]
    if not in_check(move_color, board_copy):
        return True
    return False
