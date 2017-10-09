import chess_class

# TODO: make some test boards, test chess2!!!
test_board_1 = {(4, 7): ('w', 'k'), (4, 0): ('b', 'k'), (4, 6): ('w', 'r'), (3, 1): ('b', 'r')}

test_game_2 = chess_class.GameState()
print 'Testing chess2 available_moves():'
for y in range(8):
    for x in range(8):
        if (x, y) in test_game_2.board.keys():
            moves = chess_class.available_moves((x, y), test_game_2.board)
            print 'Moves available from ({}, {}): {}'.format(x, y, len(moves))
            for move in moves:
                print '                    ({}, {})'.format(move[0], move[1])
        else:
            print 'No moves available from ({}, {})'.format(x, y)
test_moves = chess_class.available_moves((3, 6), test_game_2.board)
print 'Checking pawn moves:'
for move in test_moves:
    print move


def print_board(board):
    horizontal_separator = '-----------------------------------------'
    for y in range(8):
        print horizontal_separator
        row = '|'
        for x in range(8):
            row += ' '
            if (x, y) in board.keys():
                row += '{}{}'.format(board[(x, y)][0].lower(), board[(x, y)][1].upper())
            else:
                row += '  '
            row += ' |'
        print row
    print horizontal_separator

game = chess_class.GameState()
game.board = test_board_1

while True:
    print_board(game.board)
    print 'Enter coordinates for square to return moves/attacks from.'
    x = int(input('x: '))
    y = int(input('y: '))
    if (x, y) in game.board.keys():
        moves = chess_class.available_moves((x, y), game.board)
        print 'There are {} move(s) available from ({}, {}):'.format(len(moves), x, y)
        for move in moves:
            print move
    else:
        print 'There is no piece at ({}, {})'.format(x, y)
