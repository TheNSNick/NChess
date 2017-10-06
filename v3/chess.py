class GameState:

    colors = ['w', 'b']
    piece_types = ['p', 'r', 'n', 'b', 'q', 'k']
    move_direction = {'w': 1, 'b': -1}
    starting_ranks = {'w': 0, 'b': 7}

    def __init__(self):
        self.board = GameState.starting_board()
        self.turn = 'w'

    @staticmethod
    def starting_board():
        # board is a dict with the form: { (x, y): (color, piece_type), ... }
        starting_board = dict()
        for color in GameState.colors:
            for x in range(8):
                pawn_rank = GameState.starting_ranks[color] + GameState.move_direction[color]
                starting_board[(x, pawn_rank)] = (color, 'p')
            for i in range(2):
                rank = GameState.starting_ranks[color]
                starting_board[(i * 7, rank)] = (color, 'r')
                starting_board[(i * 5 + 1, rank)] = (color, 'n')
                starting_board[(i * 3 + 2, rank)] = (color, 'b')
            starting_board[(3, rank)] = (color, 'q')
            starting_board[(4, rank)] = (color, 'k')
        return starting_board

    def in_check(self, *color):
        if len(color) == 1:
            assert color[0] in GameState.colors, 'in_check: invalid check_color passed'
            check_color = color[0]
        else:
            check_color = self.turn
        all_opposing_attacks = []
        for coords, piece in self.board.iteritems():
            if piece[0] == check_color and piece[1] == 'k':
                king_coords = (coords[0], coords[1])
            if piece[0] != check_color:
                _, piece_attacks = self.moves_and_attacks(coords)
                all_opposing_attacks.extend(piece_attacks)
        return king_coords in all_opposing_attacks


    def moves_and_attacks_diagonally(self, move_coords):
        move_x, move_y = move_coords
        move_color = self.board[move_coords][0]
        moves = []
        attacks = []
        # up-left
        for i in range(min(move_x, move_y)):
            if (move_x - i - 1, move_y - i - 1) not in self.board.keys():
                moves.append((move_x - i - 1, move_y - i - 1))
            else:
                if self.board[(move_x - i - 1, move_y - i - 1)][0] != move_color:
                    moves.append((move_x - i - 1, move_y - i - 1))
                    attacks.append((move_x - i - 1, move_y - i - 1))
                break
        # up-right
        for i in range(min(7 - move_x, move_y)):
            if (move_x + i + 1, move_y - i - 1) not in self.board.keys():
                moves.append((move_x + i + 1, move_y - i - 1))
            else:
                if self.board[(move_x + i + 1, move_y - i - 1)][0] != move_color:
                    moves.append((move_x + i + 1, move_y - i - 1))
                    attacks.append((move_x + i + 1, move_y - i - 1))
                break
        # down-right
        for i in range(min(7 - move_x, 7 - move_y)):
            if (move_x + i + 1, move_y + i + 1) not in self.board.keys():
                moves.append((move_x + i + 1, move_y + i + 1))
            else:
                if self.board[(move_x + i + 1, move_y + i + 1)][0] != move_color:
                    moves.append((move_x + i + 1, move_y + i + 1))
                    attacks.append((move_x + i + 1, move_y + i + 1))
                break
        # down-left
        for i in range(min(move_x, 7 - move_y)):
            if (move_x - i - 1, move_y + i + 1) not in self.board.keys():
                moves.append((move_x - i - 1, move_y + i + 1))
            else:
                if self.board[(move_x - i - 1, move_y + i + 1)][0] != move_color:
                    moves.append((move_x - i - 1, move_y + i + 1))
                    attacks.append((move_x - i - 1, move_y + i + 1))
                break
        return moves, attacks

    def moves_and_attacks_orthogonally(self, move_coords):
        move_x, move_y = move_coords
        move_color = self.board[move_coords][0]
        moves = []
        attacks = []
        # left
        for i in range(move_x):
            if (move_x - i - 1, move_y) not in self.board.keys():
                moves.append((move_x - i - 1, move_y))
            else:
                if self.board[(move_x - i - 1, move_y)][0] != move_color:
                    moves.append((move_x - i - 1, move_y))
                    attacks.append((move_x - i - 1, move_y))
                break
        # up
        for i in range(move_y):
            if (move_x, move_y - i - 1) not in self.board.keys():
                moves.append((move_x, move_y - i - 1))
            else:
                if self.board[(move_x, move_y - i - 1)][0] != move_color:
                    moves.append((move_x, move_y - i - 1))
                    attacks.append((move_x, move_y - i - 1))
                break
        # right
        for i in range(7 - move_x):
            if (move_x + i + 1, move_y) not in self.board.keys():
                moves.append((move_x + i + 1, move_y))
            else:
                if self.board[(move_x + i + 1, move_y)][0] != move_color:
                    moves.append((move_x + i + 1, move_y))
                    attacks.append((move_x + i + 1, move_y))
                break
        # down
        for i in range(7 - move_y):
            if (move_x, move_y + i + 1) not in self.board.keys():
                moves.append((move_x, move_y + i + 1))
            else:
                if self.board[(move_x, move_y + i + 1)][0] != move_color:
                    moves.append((move_x, move_y + i + 1))
                    attacks.append((move_x, move_y + i + 1))
                break
        return moves, attacks

    def moves_and_attacks(self, move_coords):
        # returns valid moves from coords (and subset which are attacking moves)
        assert move_coords in self.board.keys(), 'moves_and_attacks: no piece found at {}'.format(move_coords)
        move_color, move_piece = self.board[move_coords]
        move_x, move_y = move_coords
        moves = []
        attacks = []
        if move_piece == 'p':
            # pawn movement
            if (move_x, move_y + GameState.move_direction[move_color]) not in self.board.keys():
                moves.append((move_x, move_y + GameState.move_direction[move_color]))
                if (move_x, move_y + 2 * GameState.move_direction[move_color]) not in self.board.keys():
                    moves.append((move_x, 2 * move_y + GameState.move_direction[move_color]))
            if (move_x - 1, move_y + GameState.move_direction[move_color]) in self.board.keys():
                if self.board[(move_x - 1, move_y + GameState.move_direction[move_color])][0] != move_color:
                    moves.append((move_x - 1, move_y + GameState.move_direction[move_color]))
                    attacks.append((move_x - 1, move_y + GameState.move_direction[move_color]))
            if (move_x + 1, move_y + GameState.move_direction[move_color]) in self.board.keys():
                if self.board[(move_x + 1, move_y + GameState.move_direction[move_color])][0] != move_color:
                    moves.append((move_x + 1, move_y + GameState.move_direction[move_color]))
                    attacks.append((move_x + 1, move_y + GameState.move_direction[move_color]))
        elif move_piece == 'r':
            # rook movement
            return self.moves_and_attacks_orthogonally(move_coords)
        elif move_piece == 'n':
            # knight movement
            knight_moves = [(move_x - 2, move_y - 1), (move_x - 1, move_y - 2), (move_x + 1, move_y - 2),
                            (move_x + 2, move_y - 1), (move_x - 2, move_y + 1), (move_x - 1, move_y + 2),
                            (move_x + 1, move_y + 2), (move_x + 2, move_y + 1)]
            for knight_move in knight_moves:
                if min(knight_move) >= 0 and max(knight_move) <= 7:
                    if knight_move not in self.board.keys():
                        moves.append(knight_move)
                    elif self.board[knight_move][0] != move_color:
                        moves.append(knight_move)
                        attacks.append(knight_move)
        elif move_piece == 'b':
            # bishop movement
            return self.moves_and_attacks_diagonally(move_coords)
        elif move_piece == 'q':
            ortho_moves, ortho_attacks = self.moves_and_attacks_orthogonally(move_coords)
            diag_moves, diag_attacks = self.moves_and_attacks_diagonally(move_coords)
            moves.extend(ortho_moves)
            moves.extend(diag_moves)
            attacks.extend(ortho_attacks)
            attacks.extend(diag_attacks)
        elif move_piece == 'k':
            # king moves
            king_moves = [(move_x - 1, move_y - 1), (move_x, move_y - 1), (move_x + 1, move_y - 1),
                            (move_x + 1, move_y), (move_x + 1, move_y + 1), (move_x, move_y + 1),
                            (move_x - 1, move_y + 1), (move_x - 1, move_y)]
            for king_move in king_moves:
                if min(king_move) >= 0 and max(king_move) <= 7:
                    if king_move not in self.board.keys():
                        moves.append(king_move)
                    elif self.board[king_move][0] != move_color:
                        moves.append(king_move)
                        attacks.append(king_move)
        # TODO: iterate over moves, remove invalid ones, duplicates, and ones that put move_color player in check
        # TODO: also iterate over attacks after that and remove ones that are no longer in moves
        return moves, attacks
