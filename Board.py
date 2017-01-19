import pygame
from pygame.locals import *
from Piece import *

# constants
TILE_SIZE = 75
BLACK_TILE_COLOR = (85, 85, 85)
WHITE_TILE_COLOR = (170, 170, 170)
SELECTION_BORDER_COLOR = (200, 200, 0)
SELECTION_BORDER_WIDTH = 5
SELECTION_TRAIL_FREE_COLOR = (0, 200, 200)
SELECTION_TRAIL_ATTACK_COLOR = (200, 0, 0)
SELECTION_TRAIL_ALPHA = 128


class Board:

    def __init__(self):
        self.pieces = self.generate_pieces()
        self.turn = 'WHITE'
        self.select_coords = (3, 6)

    def __iter__(self):
        return self.pieces.__iter__()

    def draw(self, display):
        self.draw_background(display)
        for piece in self:
            piece.draw(display)
        if self.select_coords is not None:
            sel_x, sel_y = self.select_coords
            select_rect = Rect(sel_x*TILE_SIZE, sel_y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(display, SELECTION_BORDER_COLOR, select_rect, SELECTION_BORDER_WIDTH)
            selected_piece = self.piece_at(self.select_coords)
            moves = selected_piece.move_squares(self)
            if moves is not None:
                for move in moves:
                    move_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
                    move_image.fill(SELECTION_TRAIL_FREE_COLOR)
                    move_image.set_alpha(SELECTION_TRAIL_ALPHA)
                    move_rect = Rect(move[0]*TILE_SIZE, move[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    display.blit(move_image, move_rect)
            attacks = selected_piece.attack_squares(self)
            if attacks is not None:
                for attack in attacks:
                    attack_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
                    attack_image.fill(SELECTION_TRAIL_ATTACK_COLOR)
                    attack_image.set_alpha(SELECTION_TRAIL_ALPHA)
                    attack_rect = Rect(attack[0] * TILE_SIZE, attack[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    display.blit(attack_image, attack_rect)

    def draw_background(self, display):
        for i in range(8):
            for j in range(8):
                draw_rect = Rect(i*TILE_SIZE, j*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if (i + j) % 2 == 0:
                    draw_color = WHITE_TILE_COLOR
                else:
                    draw_color = BLACK_TILE_COLOR
                pygame.draw.rect(display, draw_color, draw_rect)

    def first_occupied_up(self, x, y):
        for i in range(y):
            if self.piece_at((x, y - 1 - i)) is not None:
                return self.piece_at((x, y - 1 - i))
            return None

    def first_occupied_down(self, x, y):
        for i in range(7 - y):
            if self.piece_at((x, y + 1 + i)) is not None:
                return self.piece_at((x, y + 1 + i))
        return None

    def first_occupied_left(self, x, y):
        for i in range(x):
            if self.piece_at((x - 1 - i, y)) is not None:
                return self.piece_at((x - 1 - i, y))
        return None

    def first_occupied_right(self, x, y):
        for i in range(7 - x):
            if self.piece_at((x + 1 + i, y)) is not None:
                return self.piece_at((x + 1 + i, y))
        return None

    def first_occupied_upleft(self, x, y):
        for i in range(min(x, y)):
            if self.piece_at((x - 1 - i, y - 1 - i)) is not None:
                return self.piece_at((x - 1 - i, y - 1 - i))
        return None

    def first_occupied_upright(self, x, y):
        for i in range(min(7 - x, y)):
            if self.piece_at((x + 1 + i, y - 1 - i)) is not None:
                return self.piece_at((x + 1 + i, y - 1 - i))
        return None

    def first_occupied_downleft(self, x, y):
        for i in range(min(x, 7 - y)):
            if self.piece_at((x - 1 - i, y + 1 + i)) is not None:
                return self.piece_at((x - 1 - i, y + 1 + i))
        return None

    def first_occupied_downright(self, x, y):
        for i in range(min(7 - x, 7 - y)):
            if self.piece_at((x + 1 + i, y + 1 + i)) is not None:
                return self.piece_at((x + 1 + i, y + 1 + i))
        return None

    def generate_pieces(self):
        pieces = []
        for i in range(8):
            pieces.append(Pawn('BLACK', i, 1))
            pieces.append(Pawn('WHITE', i, 6))
        for i in range(2):
            pieces.append(Rook('BLACK', i*7, 0))
            pieces.append(Rook('WHITE', i*7, 7))
            pieces.append(Knight('BLACK', 1+i*5, 0))
            pieces.append(Knight('WHITE', 1+i*5, 7))
            pieces.append(Bishop('BLACK', 2+i*3, 0))
            pieces.append(Bishop('WHITE', 2+i*3, 7))
        pieces.append(Queen('BLACK', 3, 0))
        pieces.append(Queen('WHITE', 3, 7))
        pieces.append(King('BLACK', 4, 0))
        pieces.append(King('WHITE', 4, 7))
        return pieces

    def in_check(self, color):
        for piece in self:
            if isinstance(piece, King):
                if piece.color == color and piece.in_check(self):
                    return True
        return False

    def next_turn(self):
        new_turn = {'BLACK': 'WHITE', 'WHITE': 'BLACK'}
        self.turn = new_turn[self.turn]

    def piece_at(self, coords):
        for piece in self:
            if piece.x == coords[0] and piece.y == coords[1]:
                return piece
        return None
