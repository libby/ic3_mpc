
# Build battleship
#
# The ships are:
#  5 - Carrier
#  4 - Battleship
#  3 - Cruiser
#  3 - Submarine
#  2 - Destroyer

# Battleship is played on a 10x10 board

# A board configuration in "ships" form is:
#   [ (o,x,y), ... x5 ] in order as they appear above
# where:
#   o in 0,1 is an orientation
#      0: left/right
#      1: up/down
#   x,y range from 0 to 9

ship_lengths = [5,4,3,3,2]
ship_names   = ['C','B','c','s','d']

def battleship_board( ships ):
    assert len(ships) == 5
    
    board = [['.']*10 for _ in range(10)]

    error = False

    for lgth, name, (updown, x, y) in zip(ship_lengths, ship_names, ships):
        # Bounds checks
        if updown:
            if not (0 <= x < 10 and
                    0 <= y < (10 - lgth)):
                print '1 Out of bounds!'
                error = True # Out of bounds!
        else:
            if not (0 <= x < (10 - lgth) and
                    0 <= y < 10):
                print '2 Out of bounds!'
                error = True # Out of bounds!
                
        for i in range(10):
            for j in range(10):
                if updown:
                    if (x == j and
                        y <= i < y + lgth):
                        # Overlap checks                        
                        if board[i][j] != '.':
                            print '3 Overlap!'
                            error = True # Overlap!
                            board[i][j] = '\xe2'
                        else:
                            board[i][j] = name
                else:
                    if (x <= j < x + lgth and
                        y == i):
                        # Overlap checks
                        if board[i][j] != '.':
                            error = True # Overlap!
                            print '4 Overlap!'
                            board[i][j] = '\xe2'
                        else:
                            board[i][j] = name
                    
    return board, error

def print_battleship(board):
    print '\n'.join(''.join(row) for row in board)


def random_board():
    import random
    # Place randomly
    ships = []
    for i,lgth in enumerate(ship_lengths):
        updown = random.randint(0,1)
        if updown:
            x = random.randint(0,9)
            y = random.randint(0,9-lgth)
        else:
            x = random.randint(0,9-lgth)
            y = random.randint(0,9)
        ships.append( (updown, x, y) )

    # If there is an overlap, just call again recursively
    board, err = battleship_board(ships)
    if err:
        print_battleship(board)
        print 'Error'
        random_board()
    else:
        print_battleship(board)

if __name__ == '__main__':
    print 'Generating a random battleship board'
    random_board()

