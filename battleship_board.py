
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
        in_bounds_ud = (0 <= x and x < 10 and
                        0 <= y and y < (10 - lgth))
        in_bounds_lr = (0 <= x and x < (10 - lgth) and
                        0 <= y and y < 10)
        in_bounds = (in_bounds_ud and updown) or (in_bounds_lr and not updown)
        error = error or (not in_bounds)
        
        for i in range(10):
            for j in range(10):
                in_ship_ud = (x == j and 
                              y <= i and i < (y + lgth))
                in_ship_lr = (x <= j and j < (x + lgth) and
                              y == i)
                in_ship = (in_ship_ud and updown) or (in_ship_lr and not updown)

                # Overlap checks
                overlap = in_ship and board[i][j] != '.'
                error = error or (overlap)

                # Paint
                if in_ship:
                    if board[i][j] == '.':
                        board[i][j] = name
                    else:
                        board[i][j] = '\xe2'

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

