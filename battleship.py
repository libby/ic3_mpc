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
        the_living = filter(lambda is_alive: is_alive, self.alive)
        return len(the_living)

    def alive_players(self):
        alive_players = []
        for i in range(0, len(self.alive)):
          if self.alive[i]:
            alive_players.append(i + 1)
        return alive_players

    def run_round(self):
        print "Starting another round."
        print "Player's lives %s " % self.alive
        print "Player numbers %s " % self.alive_players()

        if not self.alive[self.runtime.id - 1]:
            sys.stdout.write(RED)
            print "You are dead."
            sys.stdout.write(RESET)
        
        if self.num_living() == 1:
           sys.stdout.write(GREEN)
           winner = self.alive.index(True) + 1
           print "We have a winner!"
           print "Player %d won!" % winner
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
        elif self.runtime.id == 1 or self.runtime.id == 2:
           self.guess = self.obtain_guess()
           print "Your number attack is %d" % self.guess
           g1, g2 = self.mpc_share_guess(self.guess)
           results = self.calc_round_results(g1, g2)
           print results
           results.addCallback(self.round_ready).addErrback(self.error)
           self.runtime.schedule_callback(results, lambda _: self.run_round())
        else:
           print " You are not a player node you are just a "
           g1, g2 = self.mpc_share_guess(1)
           results = self.calc_round_results(g1, g2)
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
     #  alive_player_array = [1, 2, 3]
       # return self.runtime.shamir_share([1, 2, 3], Zp, guess)
        if not self.alive[self.runtime.id - 1]:
          print "sorry you're dead ignoring your input  %s " % self.runtime.id
          return self.runtime.shamir_share(alive_player_array, Zp, None)
        else:  
          print "you're alive  your player num  %s " % self.runtime.id
          print "alive  mcp %s " % alive_player_array 
          if self.runtime.id == 1 or self.runtime.id == 2:
            print "in 1,2 "  
            g1, g2 = self.runtime.shamir_share([1, 2], Zp, guess)
          else: 
            print "in 3"
            g1, g2 = self.runtime.shamir_share([1, 2], Zp)
        print "caled g1 g2 "
        print g1
        print g2
        return [g1, g2]

    def calc_round_results(self, g1, g2):
        # Now that everybody has secret shared their inputs we can
        # compare them. We check to see if any of the players have
        # guessed another player's secret, in which case they kill
        # that player, but because this is secrete shared, we don't
        # learn anything about the guesses of the other players
        # or the secrets.
        # TODO: can we do 'or'?
        print g2

        one_dead     = (g2 == self.s1) # or (g3 == s1)
        two_dead     = (g1 == self.s2) # or (g3 == s2)

        # The results are secret shared, so we must open them before
        # we can do anything usefull with them. open in this case
        # means computing
        # open the secret shared results
        open_one_dead = self.runtime.open(one_dead)
        open_two_dead = self.runtime.open(two_dead)
        return gather_shares([open_one_dead, open_two_dead])

    def __init__(self, runtime):
        # Save the Runtime for later use
        self.runtime = runtime
        lives = [False for p in runtime.players]
        # Only two player are actually playing
        # the other's are just for MPC
        lives[0] = True
        lives[1] = True
        self.alive = lives
        print "Player's lives %s " % self.alive
        print "You are Player %d " % (runtime.id) 
        print "There are %d player in this game." % (len(runtime.players))
        # we only play with two players, the others are only for MPC
        if runtime.id == 1 or runtime.id == 2:
          sys.stdout.write(RED)
          sec_num = input("Enter a secret number for you opponent to guess (1 - 20): ")
          sys.stdout.write(RESET)
          print "Your secret is: ", sec_num
          # This is the value we will use in the protocol.
          self.sec_num = sec_num
          # This is also a secret shared value we will use in the protocol.
          self.guess = self.obtain_guess()
          print "Your number attack is %d" % self.guess

        # For the comparison protocol to work, we need a field modulus
        # bigger than 2**(l+1) + 2**(l+k+1), where the bit length of
        # the input numbers is l and k is the security parameter.
        # Further more, the prime must be a Blum prime (a prime p such
        # that p % 4 == 3 holds). The find_prime function lets us find
        # a suitable prime.
        l = runtime.options.bit_length
        k = runtime.options.security_parameter
        Zp = GF(find_prime(2**(l + 1) + 2**(l + k + 1), blum=True))

        # We must secret share our input with the other parties. They
        # will do the same and we end up with three variables
        if runtime.id == 1 or runtime.id == 2:
          print "I'm player 1 2 get my shares"
          self.s1, self.s2 = runtime.shamir_share([1, 2], Zp, self.sec_num)
          g1, g2 = runtime.shamir_share([1, 2], Zp, self.guess)
        else:
          print "I'm player 3 don't get my shares"
          self.s1, self.s2 = runtime.shamir_share([1, 2], Zp)
          g1, g2 = runtime.shamir_share([1, 2], Zp)
        print "g1 g2 calc"
        print g1
        print g2
        results = self.calc_round_results(g1, g2)
        results.addCallback(self.round_ready)
        runtime.schedule_callback(results, lambda _: self.run_round())

    def round_ready(self, results):
        p1_is_dead = results[0] 
        p2_is_dead = results[1] 
        if p1_is_dead: 
          self.alive[0] = False
        if p2_is_dead:
          self.alive[1] = False

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
