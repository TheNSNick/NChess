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
        self.flags = {'w': {'king_moved': False,
                            'queens_rook_moved': False,
                            'kings_rook_moved': False,
                            'en_passant': None
                            },
                      'b': {'king_moved': False,
                            'queens_rook_moved': False,
                            'kings_rook_moved': False,
                            'en_passant': None
                            }
                      }
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

    def can_castle_queenside(self, color):
        if self.flags[color]['king_moved'] or self.flags[color]['queens_rook_moved'] or in_check(color, self):
            return False
        else:
            for check_file in range(1, 4):
                if (GameState.starting_rank[color], check_file) in self.board.keys():
                    return False
                else:
                    for check_coords, check_piece in self.board.iteritems():
                        check_color, check_type = check_piece
                        if check_color != color:
                            if check_type == 'p':
                                if 0 <= check_coords[0] <= 4 \
                                        and check_coords[1] == GameState.starting_rank[color] + GameState.move_direction[color]:
                                    return False
                            else:
                                if (check_file, GameState.starting_rank[color]) in available_moves(check_coords, self, check_safe=True):
                                    return False
            return True

    def can_castle_kingside(self, color):
        if self.flags[color]['king_moved'] or self.flags[color]['kings_rook_moved'] or in_check(color, self):
            return False
        else:
            for check_file in range(5, 7):
                if (GameState.starting_rank[color], check_file) in self.board.keys():
                    return False
                else:
                    for check_coords, check_piece in self.board.iteritems():
                        check_color, check_type = check_piece
                        if check_color != color:
                            if check_type == 'p':
                                if 4 <= check_coords[0] \
                                        and check_coords[1] == GameState.starting_rank[color] + GameState.move_direction[color]:
                                    return False
                            else:
                                if (check_file, GameState.starting_rank[color]) in available_moves(check_coords, self, check_safe=True):
                                    return False
            return True

    def make_move(self, from_coords, to_coords):
        assert from_coords in self.board.keys(), 'GameState.make_move(): no piece found at {}'.format(from_coords)
        # move piece
        taken_piece = self.board.pop(to_coords, None)
        self.board[to_coords] = self.board.pop(from_coords)
        # castling checks
        if self.board[to_coords][1] == 'k':
            self.flags[self.turn]['king_moved'] = True
            if from_coords == (4, GameState.starting_rank[self.turn]):
                if to_coords == (2, GameState.starting_rank[self.turn]):
                    self.board[(3, GameState.starting_rank[self.turn])] = self.board.pop(0, GameState.starting_rank[self.turn])
                elif to_coords == (6, GameState.starting_rank[self.turn]):
                    self.board[(5, GameState.starting_rank[self.turn])] = self.board.pop(7, GameState.starting_rank[self.turn])
        if self.board[to_coords][1] == 'r':
            if self.board[from_coords] == (0, GameState.starting_rank[self.turn]):
                self.flags[self.turn]['queens_rook_moved'] = True
            elif self.board[from_coords] == (7, GameState.starting_rank[self.turn]):
                self.flags[self.turn]['kings_rook_moved'] = True
        # en passant check
        if self.board[to_coords][1] == 'p' and from_coords[0] != to_coords[0] and taken_piece is None:
            taken_piece = self.board.pop(to_coords[0], from_coords[1])
        # change turn and deselect
        self.turn = GameState.opposite_colors[self.turn]
        self.selected = None
        # en passant flag setting
        if self.board[to_coords][1] == 'p' and from_coords[1] == GameState.starting_rank[self.turn] \
                and to_coords[1] == GameState.starting_rank[self.turn] + 2 * GameState.move_direction[self.turn]:
            self.flags[self.turn]['en_passant'] = to_coords[0]
        else:
            self.flags[self.turn]['en_passant'] = None
        return taken_piece


def available_moves(coords, game_state, check_safe=False):
    board = game_state.board
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
        if move_y == GameState.starting_rank[move_color] + 4 * GameState.move_direction[move_color]:
            pawn_jump = game_state.flags[move_color]['en_passant']
            if pawn_jump is not None:
                if move_x - 1 == pawn_jump:
                    moves.append(move_x - 1, move_y + GameState.move_direction[move_color])
                elif move_x + 1 == pawn_jump:
                    moves.append(move_x + 1, move_y + GameState.move_direction[move_color])
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
        if game_state.can_castle_queenside(move_color):
            moves.append((2, GameState.starting_rank[move_color]))
        if game_state.can_castle_kingside(move_color):
            moves.append((6, GameState.starting_rank[move_color]))
    # reduce duplicates and invalid moves
    moves = list(set(moves))
    valid_moves = []
    for move in moves:
        if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
            # make sure the move doesn't put player in check
            if not check_safe:
                board_copy = copy.deepcopy(game_state.board)
                flags_copy = copy.deepcopy(game_state.flags)
                board_copy[move] = board_copy.pop(coords)
                game_copy = GameState()
                game_copy.board = board_copy
                game_copy.turn = game_state.turn
                game_copy.flags = flags_copy
                if not in_check(move_color, game_copy):
                    valid_moves.append(move)
            else:
                valid_moves.append(move)
    return valid_moves


def in_check(color, game_state):
    opponent_moves = []
    for find_coords in game_state.board.keys():
        if game_state.board[find_coords][0] != color:
            opponent_moves.extend(available_moves(find_coords, game_state, check_safe=True))
        if game_state.board[find_coords][0] == color and game_state.board[find_coords][1] == 'k':
            king_coords = find_coords
    return king_coords in opponent_moves
