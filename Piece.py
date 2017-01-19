import os
import copy
import pygame
from pygame.locals import *

# constants
TILE_SIZE = 75
IMAGE_ALPHA = (222, 0, 222)


class Piece:

    def __init__(self, color, x, y):
        assert color.upper() in ['BLACK', 'WHITE'], 'Invalid color given for Piece init.'
        assert 0 <= int(x) <= 7, 'Invalid x coord given for Piece init.'
        assert 0 <= int(y) <= 7, 'Invalid y coord given for Piece init.'
        self.color = color.upper()
        self.x = int(x)
        self.y = int(y)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))

    def attack_squares(self, board):
        # TO BE OVERRIDDEN BY CHILD CLASSES
        pass

    def draw(self, display):
        draw_rect = Rect(self.x*TILE_SIZE, self.y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
        display.blit(self.image, draw_rect)

    def move_squares(self, board):
        # TO BE OVERRIDDEN BY CHILD CLASSES
        pass

    def verify_move(self, board, coords):
        check_x = coords[0]
        check_y = coords[1]
        check_board = copy.copy(board)
        for piece in check_board:
            if piece.x == self.x and piece.y == self.y:
                check_board.pieces.remove(piece)
            if piece.x == check_x and piece.y == check_y:
                check_board.pieces.remove(piece)
        check_self = copy.copy(self)
        check_self.x = check_x
        check_self.y = check_y
        check_board.pieces.append(check_self)
        if board.in_check(self.color):
            return False
        return True


class Pawn(Piece):

    def __init__(self, color, x, y):
        Piece.__init__(self, color, x, y)
        file_name = '{}_pawn.png'.format(self.color.lower())
        self.image = pygame.image.load(os.path.join('gfx', file_name)).convert()
        self.image.set_colorkey(IMAGE_ALPHA)
        if self.color == 'BLACK':
            self.direction = 1
        elif self.color == 'WHITE':
            self.direction = -1

    def attack_squares(self, board):
        attacks = []
        for i in [-1, 1]:
            check_piece = board.piece_at((self.x+i, self.y+self.direction))
            if check_piece is not None:
                if check_piece.color != self.color:
                    attacks.append((self.x+i, self.y+self.direction))
        for attack in attacks:
            if not self.verify_move(board, attack):
                attacks.remove(attack)
        return attacks

    def move_squares(self, board):
        moves = []
        if board.piece_at((self.x, self.y+self.direction)) is None:
            moves.append((self.x, self.y+self.direction))
            if board.piece_at((self.x, self.y+2*self.direction)) is None:
                moves.append((self.x, self.y+2*self.direction))
        for move in moves:
            if not self.verify_move(board, move):
                moves.remove(move)
        return moves


class Rook(Piece):

    def __init__(self, color, x, y):
        Piece.__init__(self, color, x, y)
        file_name = '{}_rook.png'.format(self.color.lower())
        self.image = pygame.image.load(os.path.join('gfx', file_name)).convert()
        self.image.set_colorkey(IMAGE_ALPHA)

    def attack_squares(self, board):
        attacks = []
        up = board.first_occupied_up(self.x, self.y)
        down = board.first_occupied_down(self.x, self.y)
        left = board.first_occupied_left(self.x, self.y)
        right = board.first_occupied_right(self.x, self.y)
        directions = [up, down, left, right]
        for direction in directions:
            if direction is not None:
                if direction.color != self.color:
                    attacks.append((direction.x, direction.y))
        for attack in attacks:
            if not self.verify_move(board, attack):
                attacks.remove(attack)
        return attacks

    def move_squares(self, board):
        moves = []
        for i in range(self.y):
            if board.piece_at((self.x, self.y - 1 - i)) is None:
                moves.append((self.x, self.y - 1 - i))
            else:
                break
        for i in range(7 - self.y):
            if board.piece_at((self.x, self.y + 1 + i)) is None:
                moves.append((self.x, self.y + 1 + i))
            else:
                break
        for i in range(self.x):
            if board.piece_at((self.x - 1 - i, self.y)) is None:
                moves.append((self.x - 1 - i, self.y))
            else:
                break
        for i in range(7 - self.x):
            if board.piece_at((self.x + 1 + i, self.y)) is None:
                moves.append((self.x + 1 + i, self.y))
            else:
                break
        for move in moves:
            if not self.verify_move(board, move):
                moves.remove(move)
        return moves


class Knight(Piece):

    def __init__(self, color, x, y):
        Piece.__init__(self, color, x, y)
        file_name = '{}_knight.png'.format(self.color.lower())
        self.image = pygame.image.load(os.path.join('gfx', file_name)).convert()
        self.image.set_colorkey(IMAGE_ALPHA)

    def attack_squares(self, board):
        attacks = []
        for move in self.possible_moves():
            piece = board.piece_at(move)
            if piece is not None:
                if piece.color != self.color:
                    attacks.append(move)
        for attack in attacks:
            if not self.verify_move(board, attack):
                attacks.remove(attack)
        return attacks

    def move_squares(self, board):
        moves = []
        for move in self.possible_moves():
            if board.piece_at(move) is None:
                moves.append(move)
        for move in moves:
            if not self.verify_move(board, move):
                moves.remove(move)
        return moves

    def possible_moves(self):
        moves = []
        patterns = [(self.x - 2, self.y - 1),
                (self.x - 1, self.y - 2),
                (self.x + 1, self.y - 2),
                (self.x + 2, self.y - 1),
                (self.x - 2, self.y + 1),
                (self.x - 1, self.y + 2),
                (self.x + 1, self.y + 2),
                (self.x + 2, self.y + 1),
                ]
        for move in patterns:
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                moves.append(move)
        return moves


class Bishop(Piece):

    def __init__(self, color, x, y):
        Piece.__init__(self, color, x, y)
        file_name = '{}_bishop.png'.format(self.color.lower())
        self.image = pygame.image.load(os.path.join('gfx', file_name)).convert()
        self.image.set_colorkey(IMAGE_ALPHA)

    def attack_squares(self, board):
        attacks = []
        ul = board.first_occupied_upleft(self.x, self.y)
        ur = board.first_occupied_upright(self.x, self.y)
        dl = board.first_occupied_downleft(self.x, self.y)
        dr = board.first_occupied_downright(self.x, self.y)
        directions = [ul, ur, dl, dr]
        for direction in directions:
            if direction is not None:
                if direction.color != self.color:
                    attacks.append((direction.x, direction.y))
        for attack in attacks:
            if not self.verify_move(board, attack):
                attacks.remove(attack)
        return attacks

    def move_squares(self, board):
        moves = []
        for i in range(min(self.x, self.y)):
            if board.piece_at((self.x - 1 - i, self.y - 1 - i)) is None:
                moves.append((self.x - 1 - i, self.y - 1 - i))
            else:
                break
        for i in range(min(7 - self.x, self.y)):
            if board.piece_at((self.x + 1 + i, self.y - 1 - i)) is None:
                moves.append((self.x + 1 + i, self.y - 1 - i))
            else:
                break
        for i in range(min(7 - self.x, 7 - self.y)):
            if board.piece_at((self.x + 1 + i, self.y + 1 + i)) is None:
                moves.append((self.x + 1 + i, self.y + 1 + i))
            else:
                break
        for i in range(min(self.x, 7 - self.y)):
            if board.piece_at((self.x - 1 - i, self.y + 1 + i)) is None:
                moves.append((self.x - 1 - i, self.y + 1 + i))
            else:
                break
        for move in moves:
            if not self.verify_move(board, move):
                moves.remove(move)
        return moves


class Queen(Piece):

    def __init__(self, color, x, y):
        Piece.__init__(self, color, x, y)
        file_name = '{}_queen.png'.format(self.color.lower())
        self.image = pygame.image.load(os.path.join('gfx', file_name)).convert()
        self.image.set_colorkey(IMAGE_ALPHA)

    def attack_squares(self, board):
        attacks = []
        up = board.first_occupied_up(self.x, self.y)
        down = board.first_occupied_down(self.x, self.y)
        left = board.first_occupied_left(self.x, self.y)
        right = board.first_occupied_right(self.x, self.y)
        ul = board.first_occupied_upleft(self.x, self.y)
        ur = board.first_occupied_upright(self.x, self.y)
        dl = board.first_occupied_downleft(self.x, self.y)
        dr = board.first_occupied_downright(self.x, self.y)
        directions = [up, down, left, right, ul, ur, dl, dr]
        for direction in directions:
            if direction is not None:
                if direction.color != self.color:
                    attacks.append((direction.x, direction.y))
        for attack in attacks:
            if not self.verify_move(board, attack):
                attacks.remove(attack)
        return attacks

    def move_squares(self, board):
        moves = []
        for i in range(self.y):
            if board.piece_at((self.x, self.y - 1 - i)) is None:
                moves.append((self.x, self.y - 1 - i))
            else:
                break
        for i in range(7 - self.y):
            if board.piece_at((self.x, self.y + 1 + i)) is None:
                moves.append((self.x, self.y + 1 + i))
            else:
                break
        for i in range(self.x):
            if board.piece_at((self.x - 1 - i, self.y)) is None:
                moves.append((self.x - 1 - i, self.y))
            else:
                break
        for i in range(7 - self.x):
            if board.piece_at((self.x + 1 + i, self.y)) is None:
                moves.append((self.x + 1 + i, self.y))
            else:
                break
        for i in range(min(self.x, self.y)):
            if board.piece_at((self.x - 1 - i, self.y - 1 - i)) is None:
                moves.append((self.x - 1 - i, self.y - 1 - i))
            else:
                break
        for i in range(min(7 - self.x, self.y)):
            if board.piece_at((self.x + 1 + i, self.y - 1 - i)) is None:
                moves.append((self.x + 1 + i, self.y - 1 - i))
            else:
                break
        for i in range(min(7 - self.x, 7 - self.y)):
            if board.piece_at((self.x + 1 + i, self.y + 1 + i)) is None:
                moves.append((self.x + 1 + i, self.y + 1 + i))
            else:
                break
        for i in range(min(self.x, 7 - self.y)):
            if board.piece_at((self.x - 1 - i, self.y + 1 + i)) is None:
                moves.append((self.x - 1 - i, self.y + 1 + i))
            else:
                break
        for move in moves:
            if not self.verify_move(board, move):
                moves.remove(move)
        return moves


class King(Piece):

    def __init__(self, color, x, y):
        Piece.__init__(self, color, x, y)
        file_name = '{}_king.png'.format(self.color.lower())
        self.image = pygame.image.load(os.path.join('gfx', file_name)).convert()
        self.image.set_colorkey(IMAGE_ALPHA)

    def attack_squares(self, board):
        attacks = []
        for move in self.possible_moves():
            piece = board.piece_at(move)
            if piece is not None:
                if piece.color != self.color:
                    attacks.append(move)
        for attack in attacks:
            if not self.verify_move(board, attack):
                attacks.remove(attack)
        return attacks

    def in_check(self, board):
        up = board.first_occupied_up(self.x, self.y)
        down = board.first_occupied_down(self.x, self.y)
        left = board.first_occupied_left(self.x, self.y)
        right = board.first_occupied_right(self.x, self.y)
        for orthogonal in [up, down, left, right]:
            if orthogonal is not None:
                if orthogonal.color != self.color:
                    if isinstance(orthogonal, Rook) or isinstance(orthogonal, Queen):
                        return True
                    if isinstance(orthogonal, King) and abs(orthogonal.x - self.x) <= 1 and abs(orthogonal.y - self.y) <= 1:
                        return True
        ul = board.first_occupied_upright(self.x, self.y)
        ur = board.first_occupied_upright(self.x, self.y)
        dl = board.first_occupied_downleft(self.x, self.y)
        dr = board.first_occupied_downright(self.x, self.y)
        for diagonal in [ul, ur, dl, dr]:
            if diagonal is not None:
                if diagonal.color != self.color:
                    if isinstance(diagonal, Bishop) or isinstance(diagonal, Queen):
                        return True
                    if isinstance(diagonal, Pawn):
                        if diagonal.y == self.y - 1 and self.color == 'BLACK':
                            return True
                        if diagonal.y == self.y + 1 and self.color == 'WHITE':
                            return True
        knight_check_coords = [(self.x - 2, self.y - 1),
                               (self.x - 1, self.y - 2),
                               (self.x + 1, self.y - 2),
                               (self.x + 2, self.y - 1),
                               (self.x + 2, self.y + 1),
                               (self.x + 1, self.y + 2),
                               (self.x - 1, self.y + 2),
                               (self.x - 2, self.y + 1),
                               ]
        for knight_check in knight_check_coords:
            knight = board.piece_at(knight_check)
            if knight is not None:
                if isinstance(knight, Knight) and knight.color != self.color:
                    return True
        return False

    def move_squares(self, board):
        moves = []
        for move in self.possible_moves():
            if board.piece_at(move) is None:
                moves.append(move)
        for move in moves:
            if not self.verify_move(board, move):
                moves.remove(move)
        return moves

    def possible_moves(self):
        moves = []
        patterns = [(self.x - 1, self.y - 1),
                (self.x, self.y - 1),
                (self.x + 1, self.y - 1),
                (self.x + 1, self.y),
                (self.x + 1, self.y + 1),
                (self.x, self.y + 1),
                (self.x - 1, self.y + 1),
                (self.x - 1, self.y),
                ]
        for move in patterns:
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                moves.append(move)
        return moves
