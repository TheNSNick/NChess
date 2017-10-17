import chess_class as chess
import pygame
from pygame.locals import *
import sys
import os


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 75
FPS = 60
WHITE = (22, 22, 22)
BLACK = (233, 233, 233)
GREY = (128, 128, 128)
GOLD = (200, 200, 0)
BLUE_GREEN = (0, 200, 200)
RED = (200, 0, 0)
ALPHA = (222, 0, 222)
SELECTION_WIDTH = 5


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_clock = pygame.time.Clock()
    game = chess.GameState()
    piece_images = {'w': {'p': pygame.image.load(os.path.join('gfx', 'wp.png')).convert(),
                          'r': pygame.image.load(os.path.join('gfx', 'wr.png')).convert(),
                          'n': pygame.image.load(os.path.join('gfx', 'wn.png')).convert(),
                          'b': pygame.image.load(os.path.join('gfx', 'wb.png')).convert(),
                          'q': pygame.image.load(os.path.join('gfx', 'wq.png')).convert(),
                          'k': pygame.image.load(os.path.join('gfx', 'wk.png')).convert()},
                    'b': {'p': pygame.image.load(os.path.join('gfx', 'bp.png')).convert(),
                          'r': pygame.image.load(os.path.join('gfx', 'br.png')).convert(),
                          'n': pygame.image.load(os.path.join('gfx', 'bn.png')).convert(),
                          'b': pygame.image.load(os.path.join('gfx', 'bb.png')).convert(),
                          'q': pygame.image.load(os.path.join('gfx', 'bq.png')).convert(),
                          'k': pygame.image.load(os.path.join('gfx', 'bk.png')).convert()}
                    }
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == MOUSEBUTTONDOWN:
                click_coords = screen_to_board_coords(event.pos)
                if click_coords is not None:
                    if game.selected is None:
                        if click_coords in game.board.keys() and game.board[click_coords][0] == game.turn:
                            game.selected = click_coords
                    else:
                        if click_coords == game.selected:
                            game.selected = None
                        elif click_coords in chess.available_moves(game.selected, game):
                            taken_piece = game.make_move(game.selected, click_coords)
                            if taken_piece is not None:
                                game.taken[taken_piece[0]][taken_piece[1]] += 1
        screen.fill(GREY)
        draw_board(screen)
        draw_pieces(screen, game.board, piece_images)
        if game.selected is not None:
            draw_tile_outline(screen, game.selected)
            for possible_move in chess.available_moves(game.selected, game):
                if possible_move in game.board.keys() and game.board[possible_move][0] != game.turn:
                    draw_tile_shading(screen, possible_move, RED)
                else:
                    draw_tile_shading(screen, possible_move, BLUE_GREEN)
        pygame.display.update()
        game_clock.tick(FPS)


def draw_board(draw_surface):
    for y in range(8):
        for x in range(8):
            tile_rect = Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if (x + y) % 2 == 0:
                tile_color = BLACK
            else:
                tile_color = WHITE
            pygame.draw.rect(draw_surface, tile_color, tile_rect)


def draw_pieces(draw_surface, board, images):
    for piece_coords, piece in board.iteritems():
        piece_color = piece[0]
        piece_type = piece[1]
        draw_coords = (piece_coords[0] * TILE_SIZE, piece_coords[1] * TILE_SIZE)
        draw_image = images[piece_color][piece_type]
        draw_image.set_colorkey(ALPHA)
        draw_surface.blit(draw_image, draw_coords)


def draw_taken_pieces(taken_dict, taken_images):
    # TODO
    pass


def draw_tile_outline(draw_surface, tile_coords):
    draw_rect = (tile_coords[0] * TILE_SIZE, tile_coords[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(draw_surface, GOLD, draw_rect, SELECTION_WIDTH)


def draw_tile_shading(draw_surface, tile_coords, shade_color):
    tile_shade_surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
    tile_shade_surface.fill(shade_color)
    tile_shade_surface.set_alpha(128)
    draw_coords = (tile_coords[0] * TILE_SIZE, tile_coords[1] * TILE_SIZE)
    draw_surface.blit(tile_shade_surface, draw_coords)


def screen_to_board_coords(screen_coords):
    screen_x, screen_y = screen_coords
    if 0 <= screen_x < 8 * TILE_SIZE and 0 <= screen_y < 8 * TILE_SIZE:
        return (screen_x / TILE_SIZE, screen_y / TILE_SIZE)
    else:
        return None


def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
