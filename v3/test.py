import chess


# TODO: make some test boards


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


game = chess.GameState()
print_board(game.board)

while True:
    print 'Enter coordinates for square to return moves/attacks from.'
    x = int(input('x: '))
    y = int(input('y: '))
    if (x, y) in game.board.keys():
        moves, attacks = game.moves_and_attacks((x, y))
        print 'There are {} move(s) available from ({}, {}):'.format(len(moves), x, y)
        for move in moves:
            if move in attacks:
                print '{}*'.format(move)
            else:
                print move
        print '* denotes attacking moves ({} total)'.format(len(attacks))
    else:
        print 'There is no piece at ({}, {})'.format(x, y)
