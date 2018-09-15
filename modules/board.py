# -*- coding: utf-8 -*-
from modules.piece import BagOfPieces, canonical, contiguous
from itertools import chain, compress

######################################################################
# Possible positions of pieces relative to a corner located at (0,0) #
######################################################################
##
# Duplicates in elements
##
# https://stackoverflow.com/questions/1541797/how-do-i-check-if-there-are-duplicates-in-a-flat-list       
def no_dup(my_list):
    return(len(my_list) == len(set(my_list)))


# https://stackoverflow.com/questions/18665873/filtering-a-list-based-on-a-list-of-booleans
# Remove polyonimo taking 2 times the same value
def remove_dup(my_list):
    return(list(compress(my_list, [no_dup(i) for i in my_list])))

##
# Duplicates in the list
##
def remove_dup2(lst):
    # https://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-whilst-preserving-order
    tple = [tuple(i) for i in lst]
    seen = set()
    seen_add = seen.add
    return [list(x) for x in tple if not (x in seen or seen_add(x))]

##
# Impossible positions
##
# Impossible positions from time = 0 in the classic game (begin in the corner)
# Impossible positions from time = 1 in the 'begin at the middle' game
def is_valid_element(poly):
    return(not ((((-1, 0) in poly) and ((1, 0) in poly)) or (((0, -1) in poly) and ((0, 1) in poly))))

# poly = [(0, -1), (0, 0), (0, 1)]
# is_valid_element(poly)

##
# Main function
##
def possible_positions_pieces(max_rank):
    '''
    Get all possible pieces given a corner at relative position (0,0)
    '''
    # Different temp variables used in this code:
    # - output: all positions of polyominos of rank <= max_rank and containing (0,0)
    # - output_rank: all positions of polyominos of rank 'rank' and containing (0,0)
    # - output_rank_plus_one: all positions of polyominos of rank 'rank+1' and containing (0,0)
    output = [[(0,0)]]
    output_rank = [[(0,0)]]
    for rank in range(1, max_rank):
        output_rank_plus_one = []
        for idx in range(rank):
            # We grow each old element (of rank 'rank') to a new element (of rank 'rank+1')
            # as follows:
            # Example with idx = 1 and old_element = [(0,0), (0,1), (1,1)]:
            # Index 1 of old_element is (0,1).
            # We select (0,1) and we all contiguous elements: (-1,1), (1,1), (0,0), (0,2).
            # We obtain 4 different lists in 'elements':
            # [(0,0), (0,1), (1,1), (-1,1)], [(0,0), (0,1), (1,1), (1,1)], 
            # [(0,0), (0,1), (1,1), (0,0)], [(0,0), (0,1), (1,1), (0,2)].
            # We remove malformed polyominos (i.e. with duplicates) and retrieve:
            # [(0,0), (0,1), (1,1), (-1,1)], [(0,0), (0,1), (1,1), (0,2)].
            # Those elements are added to output_rank_plus_one    
            element_to_grows = [old_element[idx] for old_element in output_rank]
            contigu_elements_to_grows = [contiguous(e) for e in element_to_grows]
                    
            elements = [[output_rank[i] + [e] 
                    for e in contigu_elements_to_grows[i]]
                    for i in range(len(output_rank))]
            elements = list(chain.from_iterable(elements))
            elements = remove_dup(elements)
            output_rank_plus_one += elements
        output += output_rank_plus_one
        output_rank = output_rank_plus_one

    # Remove duplicated polyominos from output
    output = [sorted(i) for i in output]
    output = remove_dup2(output)
    # print(len(output))
    
    return(output)

def possible_positions_pieces_as_a_dict(max_rank, remove_impossible = True):
    output = possible_positions_pieces(max_rank)
    
    if remove_impossible:
        bool_to_keep = map(is_valid_element, output)
        output = list(compress(output, bool_to_keep))
    
    # Each possible positions pieces is related to a piece
    # We create a dictionary assigning the different positions for 
    # each piece.
    output_dict = dict()
    my_bag = BagOfPieces(None, None, max_rank)
    for poly in output:
        idx = my_bag.index(canonical(poly))
        poly_name = my_bag[idx].name
        
        if poly_name in output_dict:
            output_dict[poly_name] += [poly]
        else:
            output_dict[poly_name] = [poly]

    return(output_dict)

# # Examples:
# possible_positions_pieces_as_a_dict(1)
# possible_positions_pieces_as_a_dict(2)
# possible_positions_pieces_as_a_dict(3)
# possible_positions_pieces_as_a_dict(4)
# possible_positions_pieces_as_a_dict(5)
# for i in range(1, 6):
#     print('max rank:', i)
#     print({key: len(val) for key, val in possible_positions_pieces_as_a_dict(i).items()})
#     print('Total length:', sum(map(len, possible_positions_pieces_as_a_dict(i).values())))
#     print('\n')
# possible_positions_pieces_as_a_dict(6)
# 
# # With impossible pieces: 1, 5, 23, 99, 414
# # Without impossible pieces: 1, 5, 21, 81, 309
# possible_positions_pieces_as_a_dict(3, remove_impossible = False)


colors = ['b', 'y', 'r', 'g']
max_rank = 5
possible_positions_before_constraints = dict()
for color in colors:
    possible_positions_before_constraints[color] = possible_positions_pieces_as_a_dict(max_rank)


possible_positions_before_constraints['b'].pop('Z5', None)         
# possible_positions_before_constraints evoluate based on pieces used...
# BagOfPieces: only the names of the pieces in text.

###############
# Class Board #
###############
class Corner():
    '''
    A corner and its attributes
    '''
    def __init__(self, possible_positions_for_pieces, position = (3,4), max_rank = 5, board_size = 20):
        self.position = position
        
        # Valid positions without outside positions
        self.valid_positions = set([(x,y) 
            for x in range(-max_rank+1, max_rank) 
            for y in range(-max_rank+1, max_rank) 
            if ((abs(x)+abs(y) < max_rank) 
               and (position[0]+x >= 0) and (position[1]+y >= 0)
               and (position[0]+x < board_size) and (position[1]+y < board_size))])
       
        # We take all possible positions for pieces
        self.valid_pieces = possible_positions_for_pieces
        # We remove pieces which are not all valid positions    
        print('We are', len(self.valid_pieces['I4']))
        print(self.valid_pieces['I4'])
        
        for piece_name, positions in self.valid_pieces.items():
            #if piece_name == 'I4':
            #    print(piece_name)
                idx_keep = [set(piece).issubset(self.valid_positions) for piece in positions]
                self.valid_pieces[piece_name] = list(compress(self.valid_pieces[piece_name], idx_keep))
            #    print(self.valid_pieces[piece_name])
                
#                for piece in positions:
#                    print(set(piece))
#                    if not set(piece).issubset(self.valid_positions):
#                        #valid_pieces_COPY[piece_name].remove(piece)
#                        print('Piece removed')
        #self.valid_pieces = valid_pieces_COPY
            
        #valid_positions_from_corners


valid_pieces = possible_positions_pieces_as_a_dict(max_rank, remove_impossible = True)
for piece_name, positions in valid_pieces.items():
            print(piece_name)
            for piece in positions:
                print(set(piece))


class Board():
    '''
    Board for playing.
    With this board, we can code 1 player, 2 players and 4 players game.
    We cannot code 3 players game with this board.
    '''
    def __init__(self, gametype = '2 players 4 colors', max_rank = 5, board_size = 20):
        ##
        # Initialize parameters
        ##
        self.max_rank = max_rank   
        self.board_size = board_size
        if gametype ==    '2 players 4 colors':
            # For this game, each player begins in the corner of the board,
            # with following order of colors and players:
            # 1. blue / player 0
            # 2. yellow / player 1
            # 3. red / player 0
            # 4. green / player 1
            self.colors = ['b', 'y', 'r', 'g']
            self.players = [0, 1, 0, 1]
            
            # # Note: for 3 players 4 colors:
            # self.colors = ['b', 'y', 'r', 'g', 'b', 'y', 'r', 'g', 'b', 'y', 'r', 'g']
            # self.players = [0, 1, 2, 0, 0, 1, 2, 1, 0, 1, 2, 2]
            #         for 4 players 4 colors:
            # self.colors = ['b', 'y', 'r', 'g']
            # self.players = [0, 1, 2, 3]

            self.nb_players = len(set(self.players))
            self.corners = {
                'b': set([((board_size-1)-0,0)]),
                'y': set([(0,0)]),
                'r': set([(0,(board_size-1)-0)]),
                'g': set([((board_size-1)-0,(board_size-1)-0)])
            }
            
            # Valid positions (to be updated at each turn)
            self.valid_positions_from_corners = {
                'b': possible_positions_pieces_as_a_dict(max_rank, remove_impossible = True),
                'y': possible_positions_pieces_as_a_dict(max_rank, remove_impossible = True),
                'r': possible_positions_pieces_as_a_dict(max_rank, remove_impossible = True),
                'g': possible_positions_pieces_as_a_dict(max_rank, remove_impossible = True)            
            }
            
        else:
            raise ValueError('This gametype is not implemented yet.')
        
        self.corners_objects = dict()
        for color in self.corners.keys():
            self.corners_objects[color] = dict()
            for position in self.corners[color]:
                possible_positions_for_pieces = self.valid_positions_from_corners[color]
                self.corners_objects[color][position] = Corner(possible_positions_for_pieces, position, max_rank, board_size)
            

        self.length_of_one_turn = len(colors)
        if len(self.colors) != len(self.players):
            raise ValueError("Size of lists 'colors_order' and 'players_order' must be equal")
            
        # Create pieces for each player
        self.bags_of_pieces = dict()
        for color, player in zip(self.colors, self.players):
            self.bags_of_pieces[color] = BagOfPieces(color, player, max_rank)
                       
        # Create set of positions and borders for each player
        self.positions = dict()
        self.borders = dict()
        for color in set(self.colors):
            self.positions[color] = set()
            self.borders[color] = set()
        
        ##
        # Initialize game
        ##
        self.time = 0 # 0, 1, 2, ... to infinity
        self.period = len(self.colors) # period T after which we loop
        self.current_color = self.colors[self.time % self.period]
        self.current_player = self.players[self.time % self.period]
        
        ##
        # Valid pieces for each corner
        ##
        # https://stackoverflow.com/questions/7369247/copy-keys-to-a-new-dictionary-python
        self.piece_of_corners = dict.fromkeys(self.corners.keys(), dict())

        # Initialize
        for col in self.piece_of_corners.keys():
            self.piece_of_corners[col] = dict.fromkeys(self.corners[col], set())





xxxx

        

max_rank = 5
board_size = 20
my_board = Board('2 players 4 colors', max_rank, board_size)
for key, val in my_board.corners_objects['b'].items():
    print(val.position)
    my_valid_positions = val.valid_positions


for piece_name, positions in my_board.valid_positions_from_corners['b'].items():
    print(piece_name)
    for piece in positions:
       print(piece)
    
for piece_name, positions in my_board.valid_positions_from_corners['b'].items():
    print(len(positions))
    
    
    
LITTLE BETTER NOW.
....
        
        
        
        # https://stackoverflow.com/questions/3931541/how-to-check-if-all-of-the-following-items-are-in-a-list
        set(['a', 'b']).issubset(['a', 'b', 'c'])
        
        
    print(positions)



max_rank = 5
position_relative_pieces = 


possible_positions_pieces_as_a_dict(max_rank)








my_corner = Corner(position = (0,0))

corners_blue = list() # list of corners. End game for this player when no remaining corner
               

        initial_ok

        # Remove positions where there is already a piece

        # Remove positions which is a border of the current color

absolute_position = (0, 0)
def remove_possible_position(absolute_position, my_corner):
    '''
    Remove a possible valid position related to a corner
    '''
    position = my_corner.position
    relative_position = tuple(absolute_position[x] - position[x] for x in range(2))
    initial_ok.discard(relative_position) # remove it if present ; do nothing elsewhere
    
should inherit attributes from board...
...        
        
        self.forbidden_outside = 




##
# 
##

aa = possible_positions_pieces_as_a_dict(5)['N']


minima(list(chain.from_iterable(chain.from_iterable(possible_positions_pieces_as_a_dict(5).values()))))


# TODO:
#
# FOR EACH CORNER:
# - list of forbidden outside
# - list of forbidden colors
# - list of forbidden borders
# Then, filter all remaining possible pieces
#
# FOR EACH CORNER:
# When a piece of other color is added:
# - update list of forbidden colors
# Then filter again all remaining possible pieces
#
# When a piece of current color is added:
# - update list of forbidden colors, 
# - update list of forbidden borders
# - update list of possible pieces (remove that piece in the bag)
# Then filter again all remaining possible pieces

# We keep a dictionary of corners:
# my_corners[color][corner] == ..... all we need






# at each corner, assign a possible_positions_piece
            
            
test = possible_positions_pieces(5) # create it for each color
# Then remove elements each time piece has been used.


my_bag = BagOfPieces(None, None, 5)






            
            
            
            i = 0
            element_to_grows = [elem[i] for elem in elements]  
            contigu_elements_to_grows = [contiguous(e) for e in element_to_grows]
            
            
            
            
            elements = [elements[0] + [e] for e in contigu_elements_to_grows[0]]
            i = 1
            element_to_grows = [elem[i] for elem in elements] 
            contigu_elements_to_grows = [contiguous(e) for e in element_to_grows]
            elements = list(chain.from_iterable([[elements[i] + [e] 
                               for e in contigu_elements_to_grows[i]] 
                               for i in range(len(elements))]))

            
            
            #contigu_elements_to_grows = [contiguous(e) for e in element_to_grows]


            elements = list(zip((elements[0],) * 4, contigu_elements_to_grows[0]))
            
            
            #elements = [element_to_grows + [contig] for contig in contigu_elements_to_grows[0]]

                      
            
            element_to_grow = corner
            set(frozenset([corner]) | frozenset([contigu]) for contigu in contiguous(element_to_grow))

            
            corner 
        
        
        
        
        
        
        for col in piece_of_corners.keys():
            piece_of_corners[col] = dict.fromkeys(corners[col], set())
                

        for color, player in zip(colors, players):
            bags_of_pieces[color] = BagOfPieces(color, player, max_rank)


def in_board(pt):
    return(pt[0] < board_size and pt[0] >= 0 and pt[1] < board_size and pt[1] >= 0)




my_board = Board()


        
        bag = 
        

positions = {
'b': {(0,0), (0,1)},
'y': {(1,3)},
'r': set(),
'g': set()
}

borders = {
'b': set(),
'y': set(),
'r': set(),
'g': set()
}



# Each time we add a piece, we update:
# - all colors: corners, borders <-- only need to check piece and borders of the piece
# - current color: positions  <-- only need to add the piece

adding_piece color, piece, position...
1. checking position
2. adding position
3. updating borders (using border of the new piece only!)












 
import numpy as np
board_matrix = np.zeros((board_size, board_size), dtype=np.dtype('U1'))
board_matrix.fill(' ')
print(board_matrix)
def text_rep(board_matrix):
    print('\n'.join(''.join(str(cell) for cell in row) for row in board_matrix))
    return(None)
text_rep(board_matrix)


# 'b', 'y', 'r', 'g'

board_matrix[(board_size-1)-0,0] = 'b'
board_matrix[(board_size-1)-0,1] = 'b'
board_matrix[(board_size-1)-1,0] = 'b'
board_matrix[(board_size-1)-2,0] = 'b'
board_matrix[(board_size-1)-3,0] = 'b'
print(board_matrix)

board_matrix[0,0] = 'y'
board_matrix[0,1] = 'y'
board_matrix[0,2] = 'y'
board_matrix[1,0] = 'y'
board_matrix[1,2] = 'y'

board_matrix[0,(board_size-1)-0] = 'r'
board_matrix[0,(board_size-1)-1] = 'r'
board_matrix[0,(board_size-1)-2] = 'r'
board_matrix[1,(board_size-1)-0] = 'r'
board_matrix[1,(board_size-1)-2] = 'r'

board_matrix[(board_size-1)-0,(board_size-1)-0] = 'g'
board_matrix[(board_size-1)-0,(board_size-1)-1] = 'g'
board_matrix[(board_size-1)-1,(board_size-1)-0] = 'g'
board_matrix[(board_size-1)-2,(board_size-1)-0] = 'g'
board_matrix[(board_size-1)-3,(board_size-1)-0] = 'g'


print(board_matrix)
text_rep(board_matrix)


list(zip())

def border(poly):
    '''Finds all points at the border of a polyomino (without corners).
       Those points can be added to a polyomino to increase its rank'''
    return unique()






border(out)

out = list(zip(idx_blue[0], idx_blue[1]))

board_matrix


np.where(board_matrix == ' ', 0, 1)

color = 'b'







# ...









[((board_size-1)-0,0), ((board_size-1)-0,1), ((board_size-1)-1,0), 
       ((board_size-1)-2,0), ((board_size-1)-3,0)]



def adding_piece(poly, poly_name, color):
    '''
    Adding a piece on the board and removing it from the bag
    Poly is the polyomino translated to a valid position
    '''    
    
    
    


color = 'b'
all_positions = set(chain.from_iterable(positions.values())) | borders[color]



set(positions.values())

list(positions.values())


def forbidden_positions(color = 'b'):
    return(positions[color] | )


def update_forbidden_positions(color = 'b'):
    

def forbidden_positions_fun(color = 'b'):
    '''
    Return set of forbidden positions on the board for a specific color
    '''
    # Current color positions and borders positions
    idx_current_color = np.where(board_matrix == color)
    poly = zip(idx_current_color[0], idx_current_color[1])
    forbidden_current_color = {pt for pt in concat_map(contiguous, poly) if in_board(pt)}
    # Forbidden other colors
    idx_other_colors = np.isin(board_matrix, [color, ' '], invert=True)
    idx_other_colors = np.where(idx_other_colors)
    poly_other = zip(idx_other_colors[0], idx_other_colors[1])
    forbidden_other_colors = set(list(poly_other))
    return(forbidden_current_color | forbidden_other_colors)
    
    
forbidden_positions_fun(color = 'b')
    
def corner_positions(color = 'b'):
    # Current color positions
    idx_current_color = np.where(board_matrix == color)
    poly = zip(idx_current_color[0], idx_current_color[1])
    
corners(poly) ....



board_matrix.isin([2, 4])

import numpy as np
a = np.arange(9).reshape((3,3))
test = np.arange(5)
print np.isin(a, test)








positions = {
 'b': [((board_size-1)-0,0), ((board_size-1)-0,1), ((board_size-1)-1,0), 
       ((board_size-1)-2,0), ((board_size-1)-3,0)],
 'y': [(0,0), (0,1), (0,2), (1,0), (1,2)],
 'r': [(0,(board_size-1)-0), (0,(board_size-1)-1), (0,(board_size-1)-2),
       (1,(board_size-1)-0), (1,(board_size-1)-2)],
 'g': [((board_size-1)-0,(board_size-1)-0), ((board_size-1)-0,(board_size-1)-1),
       ((board_size-1)-1,(board_size-1)-0), ((board_size-1)-2,(board_size-1)-0),
       ((board_size-1)-3,(board_size-1)-0)]
 }
 