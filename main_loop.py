from __future__ import print_function
from builtins import input

from cmd import Cmd

from battleship_board import battleship_board, print_battleship, ship_lengths


SHIPNAMES = ('carrier', 'battleship', 'cruiser', 'submarine', 'destroyer')
SHIP_DATA = zip(SHIPNAMES, ship_lengths)


class BattleshipShell(Cmd):
    intro = ('Welcome to the MPC Battleship game. '
             'Type help or ? to list commands.\n')
    prompt = '(battleship) '
    file = None

    def do_board(self, arg):
        """Input board layout, i.e. positioning of the ships.

        Build battleship

        The ships are:

            5 - Carrier
            4 - Battleship
            3 - Cruiser
            3 - Submarine
            2 - Destroyer

        Battleship is played on a 10x10 board

        A board configuration in "ships" form is:
          [ (o,x,y), ... x5 ] in order as they appear above
        where:
          o in 0,1 is an orientation
             0: left/right
             1: up/down
          x,y range from 0 to 9

        Usage:
            just type in "board" and enter the triplet (orientation x y) for
            each ship. Example:

            (battleship) board
            carrier (length 5) default: 0 0 0? 0 3 3
            ...
        """
        ships = []
        i = 0
        for name, length in SHIP_DATA:
            ship = input(
                '{} (length {}) default: 0 0 {}? '.format(name, length, i))
            if not ship:
                ship = '0 0 {}'.format(i)
                i += 1
            ships.append(tuple(map(int, ship.split())))

        board, err = battleship_board(ships)
        if err:
            print('Error')
        else:
            self.board = board
        print_battleship(board)
        return(board)

    def do_show_board(self, arg):
        print_battleship(self.board)

    def do_recv_attack(self, arg):
        attack = input('fake attack: ')
        print(attack)
        # TODO check if the attack succeeded via MPC layer

    def do_send_attack(self, arg):
        board = self.do_board(self)
        attack_x = int(input('Input your attack coordinates (x): '))
        attack_y = int(input('Input your attack coordinates (y): '))

        if board[attack_x][attack_y] != '.':
            print('hit')
        else:
            print('miss')


if __name__ == '__main__':
    BattleshipShell().cmdloop()
