import pygame
from pygame.locals import *
import chess_functions
import os
import sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 75
FPS = 30
ALPHA_COLOR = (222, 0, 222)
WHITE = (222, 222, 222)
BLACK = (22, 22, 22)
GREY = (128, 128, 128)
SELECT_BORDER_COLOR = (222, 222, 0)
SELECT_BORDER_WIDTH = 5
MOVE_COLOR = (0, 222, 222)
ATTACK_COLOR = (222, 0, 0)


def main():
    # game initialization
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_clock = pygame.time.Clock()
    game_board = chess_functions.generate_starting_board()
    piece_images = {'w': {}, 'b': {}}
    taken_images = {'w': {}, 'b': {}}
    for piece_color in chess_functions.COLORS:
        for piece_type in ['p', 'r', 'n', 'b', 'q', 'k']:
            image_name = piece_color + piece_type + '.png'
            piece_images[piece_color][piece_type] = pygame.image.load(os.path.join('gfx', image_name)).convert()
            taken_images[piece_color][piece_type] = pygame.image.load(os.path.join('gfx_bold', image_name)).convert()
    piece_sprites = pygame.sprite.Group(generate_sprites_from_board(game_board, piece_images))
    selected_tile_coords = None
    current_turn = 'w'
    pawn_jump_flag = None
    castle_flags = {'w': {'king_moved': False, 'queen_rook_moved': False, 'king_rook_moved': False},
                    'b': {'king_moved': False, 'queen_rook_moved': False, 'king_rook_moved': False}}
    taken_pieces = {'w': {'p': 0, 'r': 0, 'n': 0, 'b': 0, 'q': 0, 'k': 0},
                    'b': {'p': 0, 'r': 0, 'n': 0, 'b': 0, 'q': 0, 'k': 0}}
    taken_sprites = pygame.sprite.Group()
    check_indicator = pygame.image.load(os.path.join('gfx', 'check_warning.png')).convert()
    check_rect = check_indicator.get_rect()
    check_rect.bottomleft = 8 * TILE_SIZE, SCREEN_HEIGHT / 2
    move_list = {'w': [], 'b': []}
    # game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == MOUSEBUTTONDOWN:
                click_coords = screen_to_board_coords(event.pos)
                if selected_tile_coords is None:
                    if click_coords in game_board.keys():
                        piece_color, piece_type = game_board[click_coords]
                        if piece_color == current_turn:
                            selected_tile_coords = click_coords
                elif selected_tile_coords == click_coords:
                    selected_tile_coords = None
                elif click_coords in chess_functions.moves_available(selected_tile_coords, game_board, castle_flags[current_turn], pawn_jump=pawn_jump_flag):
                    # get move notation
                    move_notation = generate_move_notation(game_board, selected_tile_coords, click_coords)
                    # set flags
                    _, piece_type = game_board[selected_tile_coords]
                    if piece_type == 'p' and selected_tile_coords[1] == chess_functions.STARTING_RANKS[current_turn] + chess_functions.MOVE_DIRECTION[current_turn] and click_coords[1] == chess_functions.STARTING_RANKS[current_turn] + 3 * chess_functions.MOVE_DIRECTION[current_turn]:
                        pawn_jump_flag = click_coords[0]
                    else:
                        pawn_jump_flag = None
                    if piece_type == 'k' and not castle_flags[current_turn]['king_moved']:
                        castle_flags[current_turn]['king_moved'] = True
                    if piece_type == 'r':
                        if not castle_flags[current_turn]['queen_rook_moved'] and click_coords == (0, chess_functions.STARTING_RANKS[current_turn]):
                            castle_flags[current_turn]['queen_rook_moved'] = True
                        if not castle_flags[current_turn]['king_rook_moved'] and click_coords == (7, chess_functions.STARTING_RANKS[current_turn]):
                            castle_flags[current_turn]['king_rook_moved'] = True
                    # make move
                    taken = chess_functions.make_move(selected_tile_coords, click_coords, game_board)
                    # finish up move notation and store
                    if chess_functions.in_check(chess_functions.OPPOSITE_COLOR[current_turn], game_board):
                        move_notation += '+'
                    move_list[current_turn].append(move_notation)
                    print move_notation # TODO -- remove (testing)
                    if taken is None:
                        # check for en passant and castling and adjust if needed
                        if piece_type == 'p' and click_coords[0] != selected_tile_coords[0]:
                            taken = game_board.pop((click_coords[0], click_coords[1] - chess_functions.MOVE_DIRECTION[current_turn]))
                        elif piece_type == 'k' and click_coords[0] - selected_tile_coords[0] in [2, -2]:
                            if click_coords[0] == 2:
                                game_board[(3, chess_functions.STARTING_RANKS[current_turn])] = game_board.pop((0, chess_functions.STARTING_RANKS[current_turn]))
                            elif click_coords[0] == 6:
                                game_board[(5, chess_functions.STARTING_RANKS[current_turn])] = game_board.pop((7, chess_functions.STARTING_RANKS[current_turn]))
                    if taken is not None:
                        # add to taken group, re-draw taken sprites
                        taken_color, taken_type = taken
                        taken_pieces[taken_color][taken_type] += 1
                        taken_sprites = pygame.sprite.Group(generate_sprites_from_taken(taken_pieces, taken_images))
                    # check for pawn upgrade
                    if piece_type == 'p' and click_coords[1] == chess_functions.STARTING_RANKS[chess_functions.OPPOSITE_COLOR[current_turn]]:
                        upgrade_choice = pawn_upgrade(screen, game_clock, current_turn, piece_images)
                        game_board[click_coords] = (current_turn, upgrade_choice)
                    # re-draw sprites
                    piece_sprites = pygame.sprite.Group(generate_sprites_from_board(game_board, piece_images))
                    # change turn, deselect coords
                    current_turn = chess_functions.OPPOSITE_COLOR[current_turn]
                    selected_tile_coords = None
                    # check for checkmate
                    if chess_functions.in_check(current_turn, game_board):
                        mate = True
                        for piece_coords, piece in game_board.iteritems():
                            piece_color, piece_type = piece
                            if piece_color == current_turn:
                                if len(chess_functions.moves_available(piece_coords, game_board, castle_flags[current_turn], pawn_jump=pawn_jump_flag)) > 0:
                                    mate = False
                                    break
                        if mate:
                            # TODO -- checkmate()
                            print 'Checkmate'
        # draw and update
        screen.fill(GREY)
        draw_board(screen)
        if selected_tile_coords is not None:
            draw_selection_border(screen, selected_tile_coords)
            draw_selection_moves(screen, game_board, chess_functions.moves_available(selected_tile_coords, game_board, castle_flags[current_turn], pawn_jump=pawn_jump_flag))
        piece_sprites.draw(screen)
        taken_sprites.draw(screen)
        if chess_functions.in_check(current_turn, game_board):
            screen.blit(check_indicator, check_rect)
        pygame.display.update()
        game_clock.tick(FPS)


def draw_board(draw_surface):
    for y in range(8):
        for x in range(8):
            if (x + y) % 2 == 0:
                fill_color = WHITE
            else:
                fill_color = BLACK
            fill_rect = Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(draw_surface, fill_color, fill_rect)


def draw_selection_border(draw_surface, tile_coords):
    draw_rect = Rect(tile_coords[0] * TILE_SIZE, tile_coords[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(draw_surface, SELECT_BORDER_COLOR, draw_rect, SELECT_BORDER_WIDTH)


def draw_selection_moves(draw_surface, board, draw_moves):
    for move in draw_moves:
        draw_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        if move in board.keys():
            draw_surf.fill(ATTACK_COLOR)
        else:
            draw_surf.fill(MOVE_COLOR)
        draw_surf.set_alpha(128)
        draw_surface.blit(draw_surf, (move[0] * TILE_SIZE, move[1] * TILE_SIZE))


def generate_sprites_from_board(board, images):
    sprites = []
    for coords, piece in board.iteritems():
        piece_color, piece_type = piece
        piece_sprite = pygame.sprite.Sprite()
        piece_sprite.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        piece_sprite.image.blit(images[piece_color][piece_type], (0, 0))
        piece_sprite.image.set_colorkey(ALPHA_COLOR)
        piece_sprite.rect = piece_sprite.image.get_rect()
        piece_sprite.rect.topleft = (coords[0] * TILE_SIZE, coords[1] * TILE_SIZE)
        sprites.append(piece_sprite)
    return sprites


def generate_move_notation(board, from_coords, to_coords):
    move = ''
    files = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
    _, piece_type = board[from_coords]
    if piece_type == 'k' and from_coords[0] - to_coords[0] in [2, -2]:
        if to_coords[0] == 2:
            return '0-0'
        elif to_coords[0] == 6:
            return '0-0-0'
    elif piece_type == 'p' and from_coords[0] != to_coords[0]:
        move += files[from_coords[0]] + 'x'
    elif piece_type != 'p':
        move += piece_type.upper()
        if to_coords in board.keys():
            move += 'x'
    move += files[to_coords[0]] + str(to_coords[1] + 1)
    if piece_type == 'p' and 'x' in move and to_coords not in board.keys():
        move += 'e.p.'
    return move


def generate_sprites_from_taken(taken, images):
    sprites = []
    count = {'w': {'p': 0, 'x': 0},
             'b': {'p': 0, 'x': 0}}
    colors = ['w', 'b']
    types = ['p', 'r', 'n', 'b', 'q', 'k']
    for color_ in colors:
        for type_ in types:
            for i in range(taken[color_][type_]):
                taken_sprite = pygame.sprite.Sprite()
                taken_sprite.image = pygame.Surface((TILE_SIZE / 3, TILE_SIZE / 3))
                pygame.transform.scale(images[color_][type_], (TILE_SIZE / 3, TILE_SIZE / 3), taken_sprite.image)
                taken_sprite.image.set_colorkey(ALPHA_COLOR)
                taken_sprite.rect = taken_sprite.image.get_rect()
                if type_ == 'p':
                    if color_ == 'w':
                        taken_sprite.rect.centery = SCREEN_HEIGHT / 2 + TILE_SIZE / 2
                    elif color_ == 'b':
                        taken_sprite.rect.centery = 3 * SCREEN_HEIGHT / 4 + TILE_SIZE / 2
                    taken_sprite.rect.left = 8 * TILE_SIZE + count[color_]['p'] * TILE_SIZE / 3
                    count[color_]['p'] += 1
                else:
                    if color_ == 'w':
                        taken_sprite.rect.centery = 5 * SCREEN_HEIGHT / 8 + TILE_SIZE / 2
                    elif color_ == 'b':
                        taken_sprite.rect.centery = 7 * SCREEN_HEIGHT / 8 + TILE_SIZE / 2
                    taken_sprite.rect.left = 8 * TILE_SIZE + count[color_]['x'] * TILE_SIZE / 3
                    count[color_]['x'] += 1
                sprites.append(taken_sprite)
    return sprites


def pawn_upgrade(draw_surface, clock, upgrade_color, images):
    # draws a selection screen on top of the existing board until the user chooses a piece
    selection_panel = pygame.Surface((5 * TILE_SIZE, 2 * TILE_SIZE))
    selection_panel.fill(GREY)
    for image_name, x_coord in [('r', TILE_SIZE / 5), ('n', 7 * TILE_SIZE / 5),
                                ('b', 13 * TILE_SIZE / 5), ('q', 19 * TILE_SIZE / 5)]:
        piece_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        piece_image.blit(images[upgrade_color][image_name], (0, 0))
        piece_image.set_colorkey(ALPHA_COLOR)
        selection_panel.blit(piece_image, (x_coord, TILE_SIZE / 2))
    draw_surface.blit(selection_panel, (3 * TILE_SIZE / 2, 3 * TILE_SIZE))
    pygame.display.update()
    clock.tick(FPS)
    y_coord = 7 * TILE_SIZE / 2
    click_rects = {
        'r': Rect(11 * TILE_SIZE / 5, y_coord, TILE_SIZE, TILE_SIZE),
        'n': Rect(17 * TILE_SIZE / 5, y_coord, TILE_SIZE, TILE_SIZE),
        'b': Rect(23 * TILE_SIZE / 5, y_coord, TILE_SIZE, TILE_SIZE),
        'q': Rect(29 * TILE_SIZE / 5, y_coord, TILE_SIZE, TILE_SIZE)
                   }
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == MOUSEBUTTONDOWN:
                for piece_type, piece_rect in click_rects.iteritems():
                    if piece_rect.collidepoint(event.pos):
                        return piece_type


def screen_to_board_coords(screen_coords):
    return (screen_coords[0] / TILE_SIZE, screen_coords[1] / TILE_SIZE)


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
