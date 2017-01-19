import os
import pygame
from pygame.locals import *

# constants
TILE_SIZE = 75
IMAGE_ALPHA = (222, 0, 222)


class Piece:

    def __init__(self, color):
        assert str(color).upper() in ['BLACK', 'WHITE'], 'Piece.__init__(): Invalid piece color given.'
        self.color = str(color).upper()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))

    def all_moves(self, at_x, at_y, board):
        '''Made to be overridden, this method will return ([attacks], [free_moves])'''
        pass

    def attacks(self, at_x, at_y, board):
        attacks, _ = self.all_moves(at_x, at_y, board)
        return attacks

    def draw(self, display, tile_x, tile_y):
        draw_rect = self.image.get_rect()
        draw_rect.topleft = (tile_x * TILE_SIZE, tile_y * TILE_SIZE)
        display.blit(self.image, draw_rect)

    def free_moves(self, at_x, at_y, board):
        _, moves = self.all_moves(at_x, at_y, board)
        return moves


class Pawn(Piece):

    def __init__(self, color):
        Piece.__init__(self, color)
        file_name = '{}_pawn.png'.format(self.color.lower())
        self.image = pygame.image.load(os.path.join('gfx', file_name)).convert()
        self.image.set_colorkey(IMAGE_ALPHA)

    def all_moves(self, at_x, at_y, board):
        attacks = []
        moves = []
        if (at_x, at_y + self.direction()) not in board.iterkeys():
            if board.verify_move((at_x, at_y), (at_x, at_y + self.direction())):
                moves.append((at_x, at_y + self.direction()))
                if (at_x, at_y + 2 * self.direction()) not in board.iterkeys():
                    if board.verify_move((at_x, at_y), (at_x, at_y + 2 * self.direction())):
                        moves.append((at_x, at_y + 2 * self.direction()))
        for diag_coords in board.closest_diagonal_coords(at_x, at_y):
            if diag_coords is not None:
                if diag_coords[1] - at_y == self.direction() and board[diag_coords].color != self.color:
                    if board.verify_move((at_x, at_y), diag_coords):
                        attacks.append(diag_coords)
        return attacks, moves

    def direction(self):
        directions = {'BLACK': 1, 'WHITE': -1}
        return directions[self.color]


class Rook(Piece):

    def __init__(self, color):
        Piece.__init__(self, color)
        file_name = '{}_rook.png'.format(self.color.lower())
        self.image = pygame.image.load(os.path.join('gfx', file_name)).convert()
        self.image.set_colorkey(IMAGE_ALPHA)

    def all_moves(self, at_x, at_y, board):
        at_coords = (at_x, at_y)
        attacks = []
        moves = []
        for i in range(at_y):
            up_check = (at_x, at_y - i - 1)
            if up_check not in board.iterkeys():
                if board.verify_move(at_coords, up_check):
                    moves.append(up_check)
            else:
                break
        for i in range(7 - at_y):
            down_check = (at_x, at_y + i + 1)
            if down_check not in board.iterkeys():
                if board.verify_move(at_coords, down_check):
                    moves.append(down_check)
            else:
                break
        for i in range(at_x):
            left_check = (at_x - i - 1, at_y)
            if left_check not in board.iterkeys():
                if board.verify_move(at_coords, left_check):
                    moves.append(left_check)
            else:
                break
        for i in range(7 - at_x):
            right_check = (at_x + i + 1, at_y)
            if right_check not in board.iterkeys():
                if board.verify_move(at_coords, right_check):
                    moves.append(right_check)
            else:
                break
        for block_coords in board.closest_orthogonal_coords(at_x, at_y):
            if block_coords is not None:
                if board[block_coords].color != self.color:
                    if board.verify_move(at_coords, block_coords):
                        attacks.append(block_coords)
        return attacks, moves


class Knight(Piece):

    def __init__(self, color):
        Piece.__init__(self, color)
        file_name = '{}_knight.png'.format(self.color.lower())
        self.image = pygame.image.load(os.path.join('gfx', file_name)).convert()
        self.image.set_colorkey(IMAGE_ALPHA)

    def all_moves(self, at_x, at_y, board):
        attacks = []
        moves = []
        possible = [(at_x - 2, at_y - 1),
                    (at_x - 1, at_y - 2),
                    (at_x + 1, at_y - 2),
                    (at_x + 2, at_y - 1),
                    (at_x + 2, at_y + 1),
                    (at_x + 1, at_y + 2),
                    (at_x - 1, at_y + 2),
                    (at_x - 2, at_y + 1),
                    ]
        at_coords = (at_x, at_y)
        for move in possible:
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                if move in board.iterkeys():
                    if board[move].color != self.color:
                        if board.verify_move(at_coords, move):
                            attacks.append(move)
                else:
                    if board.verify_move(at_coords, move):
                        moves.append(move)
        return attacks, moves


class Bishop(Piece):

    def __init__(self, color):
        Piece.__init__(self, color)
        file_name = '{}_bishop.png'.format(self.color.lower())
        self.image = pygame.image.load(os.path.join('gfx', file_name)).convert()
        self.image.set_colorkey(IMAGE_ALPHA)

    def all_moves(self, at_x, at_y, board):
        attacks = []
        moves = []
        at_coords = (at_x, at_y)
        for i in range(min(at_x, at_y)):
            check_move = (at_x - i - 1, at_y - i - 1)
            if check_move not in board.iterkeys():
                if board.verify_move(at_coords, check_move):
                    moves.append(check_move)
            else:
                break
        for i in range(min(7 - at_x, at_y)):
            check_move = (at_x + i + 1, at_y - i - 1)
            if check_move not in board.iterkeys():
                if board.verify_move(at_coords, check_move):
                    moves.append(check_move)
            else:
                break
        for i in range(min(at_x, 7 - at_y)):
            check_move = (at_x - i - 1, at_y + i + 1)
            if check_move not in board.iterkeys():
                if board.verify_move(at_coords, check_move):
                    moves.append(check_move)
            else:
                break
        for i in range(min(7 - at_x, 7 - at_y)):
            check_move = (at_x + i + 1, at_y + i + 1)
            if check_move not in board.iterkeys():
                if board.verify_move(at_coords, check_move):
                    moves.append(check_move)
            else:
                break
        for block_coords in board.closest_diagonal_coords(at_x, at_y):
            if block_coords is not None:
                if board[block_coords].color != self.color:
                    if board.verify_move(at_coords, block_coords):
                        attacks.append(block_coords)
        return attacks, moves


class Queen(Piece):

    def __init__(self, color):
        Piece.__init__(self, color)
        file_name = '{}_queen.png'.format(self.color.lower())
        self.image = pygame.image.load(os.path.join('gfx', file_name)).convert()
        self.image.set_colorkey(IMAGE_ALPHA)

    def all_moves(self, at_x, at_y, board):
        at_coords = (at_x, at_y)
        attacks = []
        moves = []
        for i in range(at_y):
            up_check = (at_x, at_y - i - 1)
            if up_check not in board.iterkeys():
                if board.verify_move(at_coords, up_check):
                    moves.append(up_check)
            else:
                break
        for i in range(7 - at_y):
            down_check = (at_x, at_y + i + 1)
            if down_check not in board.iterkeys():
                if board.verify_move(at_coords, down_check):
                    moves.append(down_check)
            else:
                break
        for i in range(at_x):
            left_check = (at_x - i - 1, at_y)
            if left_check not in board.iterkeys():
                if board.verify_move(at_coords, left_check):
                    moves.append(left_check)
            else:
                break
        for i in range(7 - at_x):
            right_check = (at_x + i + 1, at_y)
            if right_check not in board.iterkeys():
                if board.verify_move(at_coords, right_check):
                    moves.append(right_check)
            else:
                break
        for block_coords in board.closest_orthogonal_coords(at_x, at_y):
            if block_coords is not None:
                if board[block_coords].color != self.color:
                    if board.verify_move(at_coords, block_coords):
                        attacks.append(block_coords)
        for i in range(min(at_x, at_y)):
            check_move = (at_x - i - 1, at_y - i - 1)
            if check_move not in board.iterkeys():
                if board.verify_move(at_coords, check_move):
                    moves.append(check_move)
            else:
                break
        for i in range(min(7 - at_x, at_y)):
            check_move = (at_x + i + 1, at_y - i - 1)
            if check_move not in board.iterkeys():
                if board.verify_move(at_coords, check_move):
                    moves.append(check_move)
            else:
                break
        for i in range(min(at_x, 7 - at_y)):
            check_move = (at_x - i - 1, at_y + i + 1)
            if check_move not in board.iterkeys():
                if board.verify_move(at_coords, check_move):
                    moves.append(check_move)
            else:
                break
        for i in range(min(7 - at_x, 7 - at_y)):
            check_move = (at_x + i + 1, at_y + i + 1)
            if check_move not in board.iterkeys():
                if board.verify_move(at_coords, check_move):
                    moves.append(check_move)
            else:
                break
        for block_coords in board.closest_diagonal_coords(at_x, at_y):
            if block_coords is not None:
                if board[block_coords].color != self.color:
                    if board.verify_move(at_coords, block_coords):
                        attacks.append(block_coords)
        return attacks, moves


class King(Piece):

    def __init__(self, color):
        Piece.__init__(self, color)
        file_name = '{}_king.png'.format(self.color.lower())
        self.image = pygame.image.load(os.path.join('gfx', file_name)).convert()
        self.image.set_colorkey(IMAGE_ALPHA)

    def all_moves(self, at_x, at_y, board):
        attacks = []
        moves = []
        at_coords = (at_x, at_y)
        possible = [(at_x - 1, at_y - 1),
                    (at_x, at_y - 1),
                    (at_x + 1, at_y - 1),
                    (at_x + 1, at_y),
                    (at_x + 1, at_y + 1),
                    (at_x, at_y + 1),
                    (at_x - 1, at_y + 1),
                    (at_x - 1, at_y),
                    ]
        for move in possible:
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                if move in board.iterkeys():
                    if board[move].color != self.color:
                        if board.verify_move(at_coords, move):
                            attacks.append(move)
                else:
                    if board.verify_move(at_coords, move):
                        moves.append(move)
        return attacks, moves
