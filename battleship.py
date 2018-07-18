#!/usr/bin/env python

# Copyright 2007, 2008 VIFF Development Team.
#
# This file is part of VIFF, the Virtual Ideal Functionality Framework.
#
# VIFF is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License (LGPL) as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# VIFF is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with VIFF. If not, see <http://www.gnu.org/licenses/>.

# This example is a tribute to the original example of secure
# multi-party computation by Yao in 1982. In his example two
# millionaires meet in the street and they want to securely compare
# their fortunes. They want to do so without revealing how much they
# own to each other. This problem would be easy to solve if both
# millionaires trust a common third party, but we want to solve it
# without access to a third party.
#
# In this example the protocol is run between three millionaires and
# uses a protocol for secure integer comparison by Toft from 2005.
#
# Give a player configuration file as a command line argument or run
# the example with '--help' for help with the command line options.

from optparse import OptionParser
import viff.reactor
viff.reactor.install()
from twisted.internet import reactor

from viff.field import GF
from viff.runtime import create_runtime, gather_shares

from viff.comparison import Toft05Runtime
from viff.config import load_config
from viff.util import rand, find_prime
from viff.equality import ProbabilisticEqualityMixin
from viff.runtime import Runtime, create_runtime, make_runtime_class
import sys

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"

# We start by defining the protocol, it will be started at the bottom
# of the file.
# http://krondo.com/a-second-interlude-deferred/
class Protocol:

    def error(self, res): 
        print "in error handling"
        print res

    def num_living(self):
        print "in num livesing"
        print self.lives
        the_living = filter(lambda x: x > 0, self.lives)
        print "the living %s " % the_living
        return len(the_living)

    def alive_players(self):
        alive_players = []
        for i in range(0, len(self.lives)):
          if self.lives[i] > 0:
            alive_players.append(i + 1)
        return alive_players

    def is_alive(self): 
      return (self.lives[self.runtime.id - 1] > 0)

    def run_round(self):
        print "Starting another round."
        print "Player's lives %s " % self.lives
        print "Test"
        print "num living %s" % self.num_living()
        print "Player naumbers %s " % self.alive_players()
        print "is alive %s" % self.is_alive()
    
        if not self.is_alive():
            sys.stdout.write(RED)
            print "You are dead."
            sys.stdout.write(RESET)
        
        if self.num_living() == 1:
           sys.stdout.write(GREEN)
           winner = "TBD" #self.alive.index(True) + 1
           print "We have a winner!"
           print "Player %s won!" % winner
           sys.stdout.write(RESET)
           # shutdown the server
           self.runtime.synchronize()
           self.runtime.shutdown()
        elif self.num_living() == 0:
           sys.stdout.write(RED)
           print "Congratulation! You have destroyed each other!"
           print "No one is left alive."
           sys.stdout.write(RESET)
           # shutdown the server
           self.runtime.synchronize()
           self.runtime.shutdown()
        elif self.is_player: 
           #if self.p1_lives_prev  
           self.guess = self.obtain_guess()
           print "Your number attack is %d" % self.guess
           g1, g2 = self.mpc_share_guess(self.guess)
           results = self.check_hits(g1, g2)
           print results
           results.addCallback(self.round_ready).addErrback(self.error)
           self.runtime.schedule_callback(results, lambda _: self.run_round())
        else:
           print "You are not a player node you are just making us secure."
           g1, g2 = self.mpc_share_guess(0)
           results = self.check_hits(g1, g2)
           print results
           results.addCallback(self.round_ready).addErrback(self.error)
           self.runtime.schedule_callback(results, lambda _: self.run_round())

    # obtain guess only if they are alive
    def obtain_guess(self):
        sys.stdout.write(GREEN)
        guess = input("Take a shot at another player's secret number: ")
        sys.stdout.write(RESET)
        # This is the value we will use in the protocol.
        return guess

    def mpc_share_guess(self, guess):
        # For the comparison protocol to work, we need a field modulus
        # bigger than 2**(l+1) + 2**(l+k+1), where the bit length of
        # the input numbers is l and k is the security parameter.
        # Further more, the prime must be a Blum prime (a prime p such
        # that p % 4 == 3 holds). The find_prime function lets us find
        # a suitable prime.
        l = self.runtime.options.bit_length
        k = self.runtime.options.security_parameter
        Zp = GF(find_prime(2**(l + 1) + 2**(l + k + 1), blum=True))
        # We must secret share our input with the other parties. They
        # will do the same and we end up with three variables
        # We can only share between the remaining player, don't wait
        # for a dead person's input.
        # TODO: only require the living players to respond.
        alive_player_array = self.alive_players()
        if not self.lives[self.runtime.id - 1] > 0:
          print "sorry you're dead ignoring your input  %s " % self.runtime.id
          return self.runtime.shamir_share(alive_player_array, Zp, None)
        else:  
          print "you're alive  your player num  %s " % self.runtime.id
          print "alive  mcp %s " % alive_player_array 
          if self.is_player:
            print "in 1,2 "  
            g1, g2 = self.runtime.shamir_share([1, 2], Zp, guess)
          else: 
            print "in 3"
            g1, g2 = self.runtime.shamir_share([1, 2], Zp)
        return [g1, g2]

    # did any one hit a ship?
    def is_hit(self, guess, ship):
        hit = (guess == ship)
        open_hit = self.runtime.open(one_dead)
        return gather_shares([open_hit])

    def check_hits(self, g1, g2):
        print "calculating hits"
        p1_hit_s1 = (g2 == self.p1_ship1)
        p2_hit_s1 = (g1 == self.p2_ship1)
        p1_hit_s2 = (g2 == self.p1_ship2)
        p2_hit_s2 = (g1 == self.p2_ship2)
        p1_hit_s3 = (g2 == self.p1_ship3)
        p2_hit_s3 = (g1 == self.p2_ship3)

        open_p1_hit_s1 = self.runtime.open(p1_hit_s1)
        open_p2_hit_s1 = self.runtime.open(p2_hit_s1)
        open_p1_hit_s2 = self.runtime.open(p1_hit_s2)
        open_p2_hit_s2 = self.runtime.open(p2_hit_s2)
        open_p1_hit_s3 = self.runtime.open(p1_hit_s3)
        open_p2_hit_s3 = self.runtime.open(p2_hit_s3)
        return gather_shares([open_p1_hit_s1, open_p2_hit_s1, open_p1_hit_s2, open_p2_hit_s2, open_p1_hit_s3, open_p2_hit_s3])
        

    def calc_round_results(self, g1, g2):
        # Now that everybody has secret shared their inputs we can
        # compare them. We check to see if any of the players have
        # guessed another player's secret, in which case they kill
        # that player, but because this is secrete shared, we don't
        # learn anything about the guesses of the other players
        # or the secrets.
        # TODO: can we do 'or'?
        print g2

        one_hit = (g2 == self.p1_ship1) or  (g2 == self.p1_ship2) or (g2 == self.p1_ship3)
        two_hit = (g1 == self.p2_ship1) or (g1 == self.p2_ship2) or (g1 == self.p2_ship3)

        # The results are secret shared, so we must open them before
        # we can do anything usefull with them. open in this case
        # means computing
        # open the secret shared results
        open_one_hit = self.runtime.open(one_hit)
        open_two_hit = self.runtime.open(two_hit)
        return gather_shares([open_one_hit, open_two_hit])

    def __init__(self, runtime):
        # Save the Runtime for later use
        self.runtime = runtime
        # to start with there are no hits
        # we will record the ship hits here.
        self.hit_list = []
        self.total_num_ships = 1
        # there are only two actual players, the other
        # "players" are only there to run MPC.
        self.is_player = (runtime.id == 1 or runtime.id == 2)

        lives = [0 for p in runtime.players]
        # Only two player are actually playing
        # the other's are just for MPC
        lives[0] = 3 
        lives[1] = 3 

        self.p1_lives_prev = 3
        self.p2_lives_prev = 3

        self.lives = lives
        print "Player's lives %s " % self.lives
        print "You are Player %d " % (runtime.id) 
        print "There are %d player in this game." % (len(runtime.players))
        # we only play with two players, the others are only for MPC

        if self.is_player:
          sys.stdout.write(RED)
          ship1 = input("Enter your ship 1: ")
          ship2 = input("Enter your ship 2: ")
          ship3 = input("Enter your ship 3: ")
          sys.stdout.write(RESET)
          # This is the value we will use in the protocol.
          self.ship1 = ship1
          self.ship2 = ship2
          self.ship3 = ship3

        # For the comparison protocol to work, we need a field modulus
        # bigger than 2**(l+1) + 2**(l+k+1), where the bit length of
        # the input numbers is l and k is the security parameter.
        # Further more, the prime must be a Blum prime (a prime p such
        # that p % 4 == 3 holds). The find_prime function lets us find
        # a suitable prime.
        l = runtime.options.bit_length
        k = runtime.options.security_parameter
        Zp = GF(find_prime(2**(l + 1) + 2**(l + k + 1), blum=True))

        # We must secret share our ships with the other parties. They
        # will do the same and we end up secretly having each other's
        # ships.
        if self.is_player:
          print "I'm player 1 2 get my secret ships as"
          print "ship 1 %s " % self.ship1
          print "ship 2 %s " % self.ship2
          print "ship 3 %s " % self.ship3
          self.p1_ship1, self.p2_ship1 = runtime.shamir_share([1, 2], Zp, self.ship1)
          self.p1_ship2, self.p2_ship2 = runtime.shamir_share([1, 2], Zp, self.ship2)
          self.p1_ship3, self.p2_ship3 = runtime.shamir_share([1, 2], Zp, self.ship3)
        else:
          print "I'm here just to help with MPC. I don't affect this game."
          self.p1_ship1, self.p2_ship1 = runtime.shamir_share([1, 2], Zp)
          self.p1_ship2, self.p2_ship2 = runtime.shamir_share([1, 2], Zp)
          self.p1_ship3, self.p2_ship3 = runtime.shamir_share([1, 2], Zp)
        ## TODO: we don't neat a board for our first design.
        # self.p1_board, self.p2_board = self.init_secret_board(l, k, Zp)

        #print "printin p1 %s" % self.p1_board
        #print "printing p2 %s" % self.p2_board
        # now we have secret shared the ships, and the board 
        # the ships will not change, but we will have to update the
        # board and the guess for each round, as we will never learn
        # about the ships values, but only that we hit one, or didn't
        # hit one.

        # get back the array of the board with the ships in place.
        # results = self.place_ships_on_board()
        # start the game loop
        self.run_round()

    # TODO: we don't really need this.
    def init_secret_board(self, l, k, Zp):
       board = [0 for i in range(0, 20)]
       p1_sec_board = []
       p2_sec_board = []

       for b in board:
         if self.is_player:
           p1_cell, p2_cell = self.runtime.shamir_share([1, 2], Zp, b)
         else:
           p1_cell, p2_cell = self.runtime.shamir_share([1, 2], Zp)
         
         p1_sec_board.append(p1_cell)
         p2_sec_board.append(p2_cell)
       return p1_sec_board, p2_sec_board

    def round_ready(self, results):
        print "round ready"
        p1_hit_s1 = results[0] 
        p2_hit_s1 = results[1] 
        p1_hit_s2 = results[2] 
        p2_hit_s2 = results[3] 
        p1_hit_s3 = results[4] 
        p2_hit_s3 = results[5] 
        if p1_hit_s1 or p1_hit_s2 or p1_hit_s3: 
          self.lives[0] = self.lives[0] - 1 
        if p2_hit_s1 or p2_hit_s2 or p2_hit_s3: 
          self.lives[1] = self.lives[1] - 1 

# Parse command line arguments.
parser = OptionParser()
Toft05Runtime.add_options(parser)
options, args = parser.parse_args()

if len(args) == 0:
    parser.error("you must specify a config file")
else:
    id, players = load_config(args[0])
#print players
#print options
# Create a deferred Runtime and ask it to run our protocol when ready.
runtime_class = make_runtime_class(mixins=[Toft05Runtime, ProbabilisticEqualityMixin])
pre_runtime = create_runtime(id, players, 1, options,runtime_class)
pre_runtime.addCallback(Protocol)

# Start the Twisted event loop.
reactor.run()
