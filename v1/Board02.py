import copy
import os

import pygame
from pygame.locals import *

import Piece02

# constants
SCREEN_WIDTH = 800
TILE_SIZE = 75
BACKGROUND_COLOR = (128, 128, 128)
BLACK_TILE_COLOR = (85, 85, 85)
WHITE_TILE_COLOR = (170, 170, 170)
SELECTION_BORDER_COLOR = (200, 200, 0)
SELECTION_BORDER_WIDTH = 5
SELECTION_TRAIL_FREE_COLOR = (0, 200, 200)
SELECTION_TRAIL_ATTACK_COLOR = (200, 0, 0)
SELECTION_TRAIL_ALPHA = 128
CHECK_RECT_COLOR = (200, 0, 0)


class Board:

    def __init__(self):
        self.tiles = self.generate_board()
        self.turn = 'WHITE'
        self.select_coords = None
        self.flags = {'BLACK': {'left_rook_moved': False,
                                'right_rook_moved': False,
                                'king_moved': False,
                                'pawn_jumped': None,
                                'en_passant': False,
                                },
                      'WHITE': {'left_rook_moved': False,
                                'right_rook_moved': False,
                                'king_moved': False,
                                'pawn_jumped': None,
                                'en_passant': False,
                                }
                      }

    def __delitem__(self, key):
        self.tiles.__delitem__(key)

    def __getitem__(self, key):
        return self.tiles[key]

    def __iter__(self):
        return self.tiles.__iter__()

    def __setitem__(self, key, value):
        self.tiles.__setitem__(key, value)

    def iteritems(self):
        return self.tiles.iteritems()

    def iterkeys(self):
        return self.tiles.iterkeys()

    def itervalues(self):
        return self.tiles.itervalues()

    def pop(self, key):
        return self.tiles.pop(key)

    def draw(self, display):
        self.draw_squares(display)
        for coords, piece in self.iteritems():
            piece.draw(display, coords[0], coords[1])
        self.draw_turn_indicator(display)
        if self.in_check(self.turn):
            self.draw_check_indicator(display)
        if self.select_coords is not None:
            selection_rect = Rect(self.select_coords[0]*TILE_SIZE, self.select_coords[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(display, SELECTION_BORDER_COLOR, selection_rect, SELECTION_BORDER_WIDTH)
            select_piece = self.tiles[self.select_coords]
            for move in select_piece.free_moves(self.select_coords[0], self.select_coords[1], self):
                trail_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
                trail_rect = trail_surf.get_rect()
                trail_rect.topleft = (move[0]*TILE_SIZE, move[1]*TILE_SIZE)
                trail_surf.fill(SELECTION_TRAIL_FREE_COLOR)
                trail_surf.set_alpha(SELECTION_TRAIL_ALPHA)
                display.blit(trail_surf, trail_rect)
            for attack in select_piece.attacks(self.select_coords[0], self.select_coords[1], self):
                attack_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
                attack_rect = attack_surf.get_rect()
                attack_rect.topleft = (attack[0]*TILE_SIZE, attack[1]*TILE_SIZE)
                attack_surf.fill(SELECTION_TRAIL_ATTACK_COLOR)
                attack_surf.set_alpha(SELECTION_TRAIL_ALPHA)
                display.blit(attack_surf, attack_rect)

    def draw_check_indicator(self, display, mate=False):
        if self.in_mate(self.turn):
            check_image_file = '{}_check_mate.png'.format(self.turn.lower())
        else:
            check_image_file = '{}_check.png'.format(self.turn.lower())
        check_image = pygame.image.load(os.path.join('gfx', check_image_file)).convert()
        check_rect = check_image.get_rect()
        check_rect.topright = (SCREEN_WIDTH, 7*TILE_SIZE/2)
        display.blit(check_image, check_rect)

    def draw_pawn_promotion(self, display, promote_color):
        promote_surface = pygame.Surface((3 * TILE_SIZE, 3 * TILE_SIZE))
        promote_surface.fill(BACKGROUND_COLOR)
        file_suffixes = ['_rook.png', '_knight.png', '_bishop.png', '_queen.png']
        for i, suffix in enumerate(file_suffixes):
            file_name = os.path.join('gfx', '{}{}'.format(promote_color.lower(), suffix))
            piece_image = pygame.image.load(file_name).convert()
            piece_image.set_colorkey(Piece02.IMAGE_ALPHA)
            piece_rect = piece_image.get_rect()
            if i % 2 == 0:
                piece_rect.centerx = 5 * TILE_SIZE / 6
            else:
                piece_rect.centerx = 13 * TILE_SIZE / 6
            if i < 2:
                piece_rect.centery = 5 * TILE_SIZE / 6
            else:
                piece_rect.centery = 13 * TILE_SIZE / 6
            promote_surface.blit(piece_image, piece_rect)
        display.blit(promote_surface, (5 * TILE_SIZE / 2, 5 * TILE_SIZE / 2))

    def draw_squares(self, display):
        for i in range(8):
            for j in range(8):
                draw_rect = Rect(i*TILE_SIZE, j*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if (i + j) % 2 == 0:
                    draw_color = WHITE_TILE_COLOR
                else:
                    draw_color = BLACK_TILE_COLOR
                pygame.draw.rect(display, draw_color, draw_rect)

    def draw_turn_indicator(self, display):
        turn_image_file = '{}_turn.png'.format(self.turn.lower())
        turn_image = pygame.image.load(os.path.join('gfx', turn_image_file)).convert()
        turn_rect = turn_image.get_rect()
        turn_height = {'BLACK': 3*TILE_SIZE, 'WHITE': 9*TILE_SIZE/2}
        turn_rect.topleft = (8*TILE_SIZE, turn_height[self.turn])
        display.blit(turn_image, turn_rect)

    def closest_diagonal_coords(self, from_x, from_y):
        '''Returns a list of tuples [(coord, piece), (coord, piece), ...] in the order UL, UR, DL, DR'''
        ul_ur_dl_dr_coords = [None, None, None, None]
        for i in range(min(from_x, from_y)):
            check_coords = (from_x - i - 1, from_y - i - 1)
            if check_coords in self.iterkeys():
                ul_ur_dl_dr_coords[0] = check_coords
                break
        for i in range(min(7 - from_x, from_y)):
            check_coords = (from_x + i + 1, from_y - i - 1)
            if check_coords in self.iterkeys():
                ul_ur_dl_dr_coords[1] = check_coords
                break
        for i in range(min(from_x, 7 - from_y)):
            check_coords = (from_x - i - 1, from_y + i + 1)
            if check_coords in self.iterkeys():
                ul_ur_dl_dr_coords[2] = check_coords
                break
        for i in range(min(7 - from_x, 7 - from_y)):
            check_coords = (from_x + i + 1, from_y + i + 1)
            if check_coords in self.iterkeys():
                ul_ur_dl_dr_coords[3] = check_coords
                break
        return ul_ur_dl_dr_coords

    def closest_orthogonal_coords(self, from_x, from_y):
        u_d_l_r_coords = [None, None, None, None]
        for i in range(from_y):
            check_coords = (from_x, from_y - i - 1)
            if check_coords in self.iterkeys():
                u_d_l_r_coords[0] = check_coords
                break
        for i in range(7 - from_y):
            check_coords = (from_x, from_y + i + 1)
            if check_coords in self.iterkeys():
                u_d_l_r_coords[1] = check_coords
                break
        for i in range(from_x):
            check_coords = (from_x - i - 1, from_y)
            if check_coords in self.iterkeys():
                u_d_l_r_coords[2] = check_coords
                break
        for i in range(7 - from_x):
            check_coords = (from_x + i + 1, from_y)
            if check_coords in self.iterkeys():
                u_d_l_r_coords[3] = check_coords
                break
        return u_d_l_r_coords

    def generate_board(self):
        tiles = {}
        for i in range(8):
            tiles[(i, 1)] = Piece02.Pawn('BLACK')
            tiles[(i, 6)] = Piece02.Pawn('WHITE')
        for y, color in {0:'BLACK', 7:'WHITE'}.iteritems():
            tiles[(0, y)] = Piece02.Rook(color)
            tiles[(7, y)] = Piece02.Rook(color)
            tiles[(1, y)] = Piece02.Knight(color)
            tiles[(6, y)] = Piece02.Knight(color)
            tiles[(2, y)] = Piece02.Bishop(color)
            tiles[(5, y)] = Piece02.Bishop(color)
            tiles[(3, y)] = Piece02.Queen(color)
            tiles[(4, y)] = Piece02.King(color)
        # TESTING
        #tiles[(4, 5)] = Piece02.Pawn('BLACK')
        #tiles[(3, 3)] = Piece02.Bishop('WHITE')
        #tiles[(4, 3)] = Piece02.Queen('WHITE')
        return tiles

    def in_check(self, check_color):
        assert check_color in ['BLACK', 'WHITE'], 'Board02.in_check: Invalid color passed.'
        # find king
        for coord, piece in self.iteritems():
            if piece.color == check_color and isinstance(piece, Piece02.King):
                king_x, king_y = coord
                break
        # check orthogonals
        for coord in self.closest_orthogonal_coords(king_x, king_y):
            if coord is not None:
                check_piece = self[coord]
                if check_piece.color != check_color:
                    if isinstance(check_piece, Piece02.Rook) or isinstance(check_piece, Piece02.Queen):
                        return True
                    if isinstance(check_piece, Piece02.King):
                        if -1 <= king_x - coord[0] <= 1 and -1 <= king_y - coord[1] <= 1:
                            return True
        # check diagonals
        for coord in self.closest_diagonal_coords(king_x, king_y):
            if coord is not None:
                check_piece = self[coord]
                if check_piece.color != check_color:
                    if isinstance(check_piece, Piece02.Bishop) or isinstance(check_piece, Piece02.Queen):
                        return True
                    if isinstance(check_piece, Piece02.Pawn) and (coord[0] - king_x == 1 or coord[0] - king_x == -1):
                        if coord[1] + check_piece.direction() == king_y:
                            return True
                    if isinstance(check_piece, Piece02.King):
                        if -1 <= king_x - coord[0] <= 1 and -1 <= king_y - coord[1] <= 1:
                            return True
        # check knights
        knight_moves = [(king_x - 2, king_y - 1),
                        (king_x - 1, king_y - 2),
                        (king_x + 1, king_y - 2),
                        (king_x + 2, king_y - 1),
                        (king_x + 2, king_y + 1),
                        (king_x + 1, king_y + 2),
                        (king_x - 1, king_y + 2),
                        (king_x - 2, king_y + 1), ]
        for coord in knight_moves:
            if coord in self.iterkeys():
                check_piece = self[coord]
                if check_piece.color != check_color and isinstance(check_piece, Piece02.Knight):
                    return True
        return False

    def in_mate(self, check_color):
        if self.in_check(check_color):
            available_moves = []
            for coord, piece in self.iteritems():
                if piece.color == check_color:
                    a, m = piece.all_moves(coord[0], coord[1], self)
                    available_moves.extend(a + m)
            if len(available_moves) == 0:
                return True
        return False

    def make_move(self, from_coords, to_coords):
        pass
        # TODO

    def next_turn(self):
        next = {'BLACK': 'WHITE', 'WHITE': 'BLACK'}
        self.turn = next[self.turn]

    def return_board_copy(self):
        new_copy = Board()
        new_copy.tiles = copy.deepcopy(self.tiles)
        new_copy.turn = copy.copy(self.turn)
        new_copy.select_coords = copy.copy(self.select_coords)
        return new_copy

    def verify_move(self, from_coords, to_coords):
        hold_piece = None
        good_move = True
        if to_coords in self.iterkeys():
            hold_piece = self.pop(to_coords)
        self[to_coords] = self.pop(from_coords)
        if self.in_check(self.turn):
            good_move = False
        self[from_coords] = self.pop(to_coords)
        if hold_piece is not None:
            self[to_coords] = hold_piece
        return good_move
