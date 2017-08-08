import chessfunctions as chess

pieces = chess.generate_new_pieces()
pieces[(4, 4)] = 'bn'
pieces[chess.convert_notation_to_coords('C5')] = 'wn'


def test_display(pieces_dict):
    for y in range(8):
        row = '|'
        for x in range(8):
            if (x, y) in pieces_dict.keys():
                row += pieces_dict[(x, y)]
            else:
                row += '--'
            row += '|'
        print row


def print_moves_and_attacks(coords, pieces_dict):
    moves = chess.return_valid_moves(coords, pieces_dict)
    attacks = chess.return_valid_attacks(coords, pieces_dict)
    print 'The {} at coords {} can move to:'.format(pieces_dict[coords], coords)
    for move in moves:
        print move
    print '({})'.format(len(moves))
    print 'The {} at {} can attack at:'.format(pieces_dict[coords], chess.convert_coords_to_notation(coords))
    for attack in attacks:
        print attack
    print '({})'.format(len(attacks))

test_display(pieces)
print_moves_and_attacks((4, 4), pieces)
print_moves_and_attacks((2, 3), pieces)
