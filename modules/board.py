# -*- coding: utf-8 -*-
from modules.piece import BagOfPieces

###############
# Class Board #
###############

# Order of colors and players:
# 1. blue / player 0
# 2. yellow / player 1
# 3. red / player 0
# 4. green / player 1

max_rank = 5

remaining_pieces = {
    'blue': BagOfPieces('blue', 0, max_rank),
    'yellow': BagOfPieces('yellow', 1, max_rank),
    'red': BagOfPieces('red', 0, max_rank),
    'green': BagOfPieces('green', 1, max_rank)
    }

played_pieces = []



remaining_pieces['blue'][3].color # blue
remaining_pieces['blue'][3].name # V3

