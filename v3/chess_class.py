import copy


class GameState:

    colors = ['w', 'b']
    starting_rank = {'w': 7, 'b': 0}
    move_direction = {'w': -1, 'b': 1}
    opposite_colors = {'w': 'b',
                       'b': 'w'}

    @staticmethod
    def starting_board():
        # board is in the form of a dict: {(x, y): (color, type), ... }
        board = {}
        for color in GameState.colors:
            for x in range(8):
                pawn_rank = GameState.starting_rank[color] + GameState.move_direction[color]
                board[(x, pawn_rank)] = (color, 'p')
            for i in range(2):
                board[(i * 7, GameState.starting_rank[color])] = (color, 'r')
                board[(i * 5 + 1, GameState.starting_rank[color])] = (color, 'n')
                board[(i * 3 + 2, GameState.starting_rank[color])] = (color, 'b')
            board[(3, GameState.starting_rank[color])] = (color, 'q')
            board[(4, GameState.starting_rank[color])] = (color, 'k')
        return board

    def __init__(self):
        self.turn = 'w'
        self.board = GameState.starting_board()
        self.selected = None
        self.taken = {'w': {'p': 0,
                            'r': 0,
                            'n': 0,
                            'b': 0,
                            'q': 0},
                      'b': {'p': 0,
                            'r': 0,
                            'n': 0,
                            'b': 0,
                            'q': 0}
                      }

    def make_move(self, from_coords, to_coords):
        assert from_coords in self.board.keys(), 'GameState.make_move(): no piece found at {}'.format(from_coords)
        taken_piece = self.board.pop(to_coords, None)
        self.board[to_coords] = self.board.pop(from_coords)
        self.turn = GameState.opposite_colors[self.turn]
        self.selected = None
        return taken_piece


def available_moves(coords, board, check_safe=False):
    assert coords in board.keys(), 'available_moves: no piece found at {} in board given'.format(coords)
    move_x, move_y = coords
    move_color, move_piece = board[coords]
    moves = []
    if move_piece == 'p':
        # pawn movement
        check_move = (move_x, move_y + GameState.move_direction[move_color])
        if check_move not in board.keys():
            moves.append(check_move)
            check_move_2 = (move_x, move_y + 2 * GameState.move_direction[move_color])
            if check_move_2 not in board.keys():
                moves.append(check_move_2)
        attack_left = (move_x - 1, move_y + GameState.move_direction[move_color])
        if attack_left in board.keys():
            if board[attack_left][0] != move_color:
                moves.append(attack_left)
        attack_right = (move_x + 1, move_y + GameState.move_direction[move_color])
        if attack_right in board.keys():
            if board[attack_right][0] != move_color:
                moves.append(attack_right)
    if move_piece == 'r' or move_piece == 'q':
        # rook/half-queen movement
        for up in range(move_y):
            check_up = (move_x, move_y - 1 - up)
            if check_up not in board.keys():
                moves.append(check_up)
            else:
                if board[check_up][0] != move_color:
                    moves.append(check_up)
                break
        for down in range(7 - move_y):
            check_down = (move_x, move_y + 1 + down)
            if check_down not in board.keys():
                moves.append(check_down)
            else:
                if board[check_down][0] != move_color:
                    moves.append(check_down)
                break
        for left in range(move_x):
            check_left = (move_x - 1 - left, move_y)
            if check_left not in board.keys():
                moves.append(check_left)
            else:
                if board[check_left][0] != move_color:
                    moves.append(check_left)
                break
        for right in range(7 - move_x):
            check_right = (move_x + 1 + right, move_y)
            if check_right not in board.keys():
                moves.append(check_right)
            else:
                if board[check_right][0] != move_color:
                    moves.append(check_right)
                break
    if move_piece == 'n':
        # knight movement
        knight_moves = [(move_x - 2, move_y - 1), (move_x - 1, move_y - 2),
                        (move_x + 1, move_y - 2), (move_x + 2, move_y - 1),
                        (move_x + 2, move_y + 1), (move_x + 1, move_y + 2),
                        (move_x - 1, move_y + 2), (move_x - 2, move_y + 1)
                        ]
        for knight_move in knight_moves:
            if knight_move not in board.keys():
                moves.append(knight_move)
            elif board[knight_move][0] != move_color:
                moves.append(knight_move)
    if move_piece == 'b' or move_piece == 'q':
        # bishop/half-queen movement
        for upleft in range(min(move_x, move_y)):
            check_upleft = (move_x - 1 - upleft, move_y - 1 - upleft)
            if check_upleft not in board.keys():
                moves.append(check_upleft)
            else:
                if board[check_upleft][0] != move_color:
                    moves.append(check_upleft)
                break
        for upright in range(min(7 - move_x, move_y)):
            check_upright = (move_x + 1 + upright, move_y - 1 - upright)
            if check_upright not in board.keys():
                moves.append(check_upright)
            else:
                if board[check_upright][0] != move_color:
                    moves.append(check_upright)
                break
        for downright in range(min(7 - move_x, 7 - move_y)):
            check_downright = (move_x + 1 + downright, move_y + 1 + downright)
            if check_downright not in board.keys():
                moves.append(check_downright)
            else:
                if board[check_downright][0] != move_color:
                    moves.append(check_downright)
                break
        for downleft in range(min(move_x, 7 - move_y)):
            check_downleft = (move_x - 1 - downleft, move_y + 1 + downleft)
            if check_downleft not in board.keys():
                moves.append(check_downleft)
            else:
                if board[check_downleft][0] != move_color:
                    moves.append(check_downleft)
                break
    if move_piece == 'k':
        # king movement
        king_moves = [(move_x - 1, move_y - 1), (move_x, move_y - 1),
                      (move_x + 1, move_y - 1), (move_x + 1, move_y),
                      (move_x + 1, move_y + 1), (move_x, move_y + 1),
                      (move_x - 1, move_y + 1), (move_x - 1, move_y)
                      ]
        for king_move in king_moves:
            if king_move not in board.keys():
                moves.append(king_move)
            elif board[king_move][0] != move_color:
                moves.append(king_move)
    # reduce duplicates and invalid moves
    moves = list(set(moves))
    valid_moves = []
    for move in moves:
        if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
            # make sure the move doesn't put player in check
            if not check_safe:
                board_copy = copy.deepcopy(board)
                board_copy[move] = board_copy.pop(coords)
                if not in_check(move_color, board_copy):
                    valid_moves.append(move)
            else:
                valid_moves.append(move)
    return valid_moves


def in_check(color, board):
    opponent_moves = []
    for find_coords in board.keys():
        if board[find_coords][0] != color:
            opponent_moves.extend(available_moves(find_coords, board, check_safe=True))
        if board[find_coords][0] == color and board[find_coords][1] == 'k':
            king_coords = find_coords
    return king_coords in opponent_moves
