# -*- coding: utf-8 -*-
import os
my_dir = os.path.expanduser('~/Documents/GitHub/blokai/')
os.chdir(my_dir) # change directory

# Example with piece Z4
from modules.piece import Piece, corners
my_piece = Piece([(3, -1), (3, 0), (4, 0), (4, 1)], 'Z4')
print(my_piece)
print(len(my_piece))
my_piece.text_repr()
my_piece.summary()
my_piece.summary(with_corners = False)
my_piece.size()
my_piece.nb_of_repr()
print(my_piece.forms['r'])
print(corners(my_piece.forms['r']))

# Bag of pieces
from modules.piece import BagOfPieces
bag = BagOfPieces(color = 'blue', player = 0)
[bag[i].text_repr() for i in range(len(bag))]
[bag[i].summary() for i in range(len(bag))]
bag.color # blue (color of the bag)
bag[8].color # blue (color of the piece inside the bag)


# *** Some links ***
# https://www.cc.gatech.edu/~isbell/classes/2003/cs4600_fall/projects/project2.html
#
# https://project.dke.maastrichtuniversity.nl/games/files/phd/Nijssen_thesis.pdf :
# (2013)
# see 3.4.3 and Fig 3.7
#
# http://artemis.library.tuc.gr/DT2014-0060/DT2014-0060.pdf
# (2014)

# http://www.eecg.toronto.edu/~choijon5/pubs/FPT2013_competition.pdf
# (2013)
#


# *** General tasks ***
# 1. program game rules
# 1.a pieces: OK
# 1.b board
#   - create board
#   - find empty corners on the board for current player,
#   - find list of couples (piece, orientation) available at a turn
# 1.c general game
#   - alternating players and user decision of playing
#   - alternating players and random decision of playing
# 1.d end of game
#   - pass when no more available move
#   - computation of score
# 1.e checking game carefully
#
# 2. algorithm
# 2.a old methods and try them
# 2.b new




