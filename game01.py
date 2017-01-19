import os
import sys
import pygame
from pygame.locals import *

# CONSTANTS
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30
TILE_SIZE = 75
IMAGE_PATH = 'gfx'
IMAGE_ALPHA_COLOR = (222, 0, 222)
BLACK_TILE_COLOR = (85, 85, 85)
WHITE_TILE_COLOR = (170, 170, 170)
SELECTION_BORDER_COLOR = (200, 200, 0)
SELECTION_BORDER_WIDTH = 5
SELECTION_TRAIL_FREE_COLOR = (0, 200, 200)
SELECTION_TRAIL_ATTACK_COLOR = (200, 0, 0)
SELECTION_TRAIL_ALPHA = 128


class Piece:

    def __init__(self, color, type, x, y):
        assert color in ['black', 'white'], 'Invalid color given for Piece init.'
        assert type in ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king'], 'Invalid type'
        assert 0 <= x <= 7, 'Invalid x coord given for Piece init.'
        assert 0 <= y <= 7, 'Invalid y coord given for Piece init.'
        self.color = color
        self.type = type
        self.x = x
        self.y = y
        image_file = '{}_{}.png'.format(self.color, self.type)
        self.image = pygame.image.load(os.path.join(IMAGE_PATH, image_file)).convert()
        self.image.set_colorkey(IMAGE_ALPHA_COLOR)

    def check_squares(self, board):
        if self.type == 'pawn':
            return self.check_pawn_squares()
        elif self.type == 'rook':
            return self.check_rook_squares(board)
        elif self.type == 'knight':
            return self.check_knight_squares()
        elif self.type == 'bishop':
            return self.check_bishop_squares(board)
        elif self.type == 'queen':
            return self.check_queen_squares(board)
        elif self.type == 'king':
            return self.check_king_squares()

    def check_pawn_squares(self):
        direction = {'black': 1, 'white': -1}
        return [(self.x-1, self.y+direction[self.color]), (self.x+1, self.y+direction[self.color])]

    def check_rook_squares(self, board):
        free_squares, check_squares = self.orthogonal_squares(board)
        return free_squares + check_squares

    def check_knight_squares(self):
        return [(self.x - 2, self.y - 1),
                (self.x - 1, self.y - 2),
                (self.x + 1, self.y - 2),
                (self.x + 2, self.y - 1),
                (self.x - 2, self.y + 1),
                (self.x - 1, self.y + 2),
                (self.x + 1, self.y + 2),
                (self.x + 2, self.y + 1),]

    def check_bishop_squares(self, board):
        free_squares, check_squares = self.diagonal_squares(board)
        return free_squares + check_squares

    def check_queen_squares(self, board):
        free_diags, check_diags = self.diagonal_squares(board)
        free_orthogs, check_orthogs = self.orthogonal_squares(board)
        return free_diags + check_diags + free_orthogs + check_orthogs

    def check_king_squares(self):
        return [(self.x - 1, self.y - 1),
                (self.x, self.y - 1),
                (self.x + 1, self.y - 1),
                (self.x + 1, self.y),
                (self.x + 1, self.y + 1),
                (self.x, self.y + 1),
                (self.x - 1, self.y + 1),
                (self.x - 1, self.y),]

    def draw(self, display):
        draw_rect = self.image.get_rect()
        draw_rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)
        display.blit(self.image, draw_rect)

    def diagonal_squares(self, board):
        free_squares = []
        attack_squares = []
        # up-left
        for i in range(min(self.x, self.y)):
            check_coords = (self.x-i-1, self.y-i-1)
            check_piece = board.piece_at(check_coords)
            if check_piece is None:
                free_squares.append(check_coords)
            else:
                if check_piece.color != self.color:
                    attack_squares.append(check_coords)
                break
        # up-right
        for i in range(min(7 - self.x, self.y)):
            check_coords = (self.x+i+1, self.y-i-1)
            check_piece = board.piece_at(check_coords)
            if check_piece is None:
                free_squares.append(check_coords)
            else:
                if check_piece.color != self.color:
                    attack_squares.append(check_coords)
                break
        # down-left
        for i in range(min(self.x, 7-self.y)):
            check_coords = (self.x-i-1, self.y+i+1)
            check_piece = board.piece_at(check_coords)
            if check_piece is None:
                free_squares.append(check_coords)
            else:
                if check_piece.color != self.color:
                    attack_squares.append(check_coords)
                break
        # right
        for i in range(min(7 - self.x, 7 - self.y)):
            check_coords = (self.x+i+1, self.y+i+1)
            check_piece = board.piece_at(check_coords)
            if check_piece is None:
                free_squares.append(check_coords)
            else:
                if check_piece.color != self.color:
                    attack_squares.append(check_coords)
                break
        return free_squares, attack_squares

    def orthogonal_squares(self, board):
        free_squares = []
        attack_squares = []
        # up
        for i in range(self.y):
            check_coords = (self.x, self.y-i-1)
            check_piece = board.piece_at(check_coords)
            if check_piece is None:
                free_squares.append(check_coords)
            else:
                if check_piece.color != self.color:
                    attack_squares.append(check_coords)
                break
        # down
        for i in range(7 - self.y):
            check_coords = (self.x, self.y+i+1)
            check_piece = board.piece_at(check_coords)
            if check_piece is None:
                free_squares.append(check_coords)
            else:
                if check_piece.color != self.color:
                    attack_squares.append(check_coords)
                break
        # left
        for i in range(self.x):
            check_coords = (self.x-i-1, self.y)
            check_piece = board.piece_at(check_coords)
            if check_piece is None:
                free_squares.append(check_coords)
            else:
                if check_piece.color != self.color:
                    attack_squares.append(check_coords)
                break
        # right
        for i in range(7 - self.x):
            check_coords = (self.x+i+1, self.y)
            check_piece = board.piece_at(check_coords)
            if check_piece is None:
                free_squares.append(check_coords)
            else:
                if check_piece.color != self.color:
                    attack_squares.append(check_coords)
                break
        return free_squares, attack_squares


class Board:

    def __init__(self):
        self.pieces = self.new_pieces()
        self.turn = 'white'
        self.selected = None

    def __iter__(self):
        return self.pieces.__iter__()

    def check(self, check_coords=None, check_color=None):
        check_squares = []
        if check_color is None:
            check_color = self.turn
        for piece in self:
            if piece.type == 'king' and piece.color == check_color and check_coords is None:
                check_coords = (piece.x, piece.y)
            elif piece.color != self.turn:
                check_squares.extend(piece.check_squares(self))
        if check_coords in check_squares:
            return True
        else:
            return False

    def draw(self, display):
        self.draw_background(display)
        for piece in self:
            piece.draw(display)
        self.draw_selection_border(display)

    def draw_background(self, display):
        for i in range(8):
            for j in range(8):
                tile_rect = (i*TILE_SIZE, j*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if (i + j) % 2 == 0:
                    tile_color = WHITE_TILE_COLOR
                else:
                    tile_color = BLACK_TILE_COLOR
                pygame.draw.rect(display, tile_rect, tile_color)

    def draw_selection_border(self, display):
        if self.selected is not None:
            selection_rect = Rect(self.selected[0]*TILE_SIZE, self.selected[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(display, SELECTION_BORDER_COLOR, selection_rect, SELECTION_BORDER_WIDTH)

    def draw_selection_trail(self, display):
        if self.selected is not None:
            selected_piece = self.piece_at(self.selected)
            free_squares, attack_squares = selected_piece.get

    def new_pieces(self):
        pieces = {}
        for i in range(8):
            pieces[(i, 1)] = Piece('black', 'pawn', i, 1)
            pieces[(i, 6)] = Piece('white', 'pawn', i, 6)
        for i in range(2):
            pieces[(i*7, 0)] = Piece('black', 'rook', i*7, 0)
            pieces[(i*7, 7)] = Piece('white', 'rook', i*7, 7)
            pieces[(1+i*5, 0)] = Piece('black', 'knight', 1+i*5, 0)
            pieces[(1+i*5, 7)] = Piece('white', 'knight', 1+i*5, 7)
            pieces[(2+i*3, 0)] = Piece('black', 'bishop', 2+i*3, 0)
            pieces[(2+i*3, 7)] = Piece('white', 'bishop', 2+i*3, 7)
        pieces[(3, 0)] = Piece('black', 'queen', 3, 0)
        pieces[(3, 7)] = Piece('white', 'queen', 3, 7)
        pieces[(4, 0)] = Piece('black', 'king', 4, 0)
        pieces[(4, 7)] = Piece('white', 'king', 4, 7)
        return pieces

    def next_turn(self):
        next_turn = {'black': 'white', 'white': 'black'}
        self.turn = next_turn[self.turn]

    def piece_at(self, coords):
        if coords in self.pieces.keys():
            return self.pieces[coords]
        else:
            return None

    def select_coords(self, coords):
        if self.selected is not None:
            if coords == self.selected:
                self.selected = None
        else:
            select_piece = self.piece_at(coords)
            if select_piece is not None:
                if select_piece.color == self.turn:
                    self.selected = coords
