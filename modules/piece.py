# -*- coding: utf-8 -*-
from itertools import chain
from itertools import compress
from collections import OrderedDict

'''
   Generate polyominos and their symmetries.
   
   Sources:
       https://wiki.haskell.org/The_Monad.Reader/Issue5/Generating_Polyominoes
       https://rosettacode.org/wiki/Free_polyominoes_enumeration#Python
       http://blokusstrategy.com/piece-names/ (for piece names)
   
   Each polyomino is represented as a list of 2 dimensional tuples.
   
   For example, a representation of L4 is the list: 
       [(0, 0), (0, 1), (0, 2), (1, 0)]
   and this is printed on a matrix as:
       X X X
       X
   
   The canonical representation of a polyomino is the smallest element of all
   plane symmetries of this polyomino.
   (smallest element using lexicographic order)
   The canonical representation of L4 is called L4_c and printed as:
       X X X
       X
   
   From this canonical representation, we deduce r, rr, rrr, s, rs, rrs, rrrs, 
   where:
   - r is 90 degree rotation to the right,
   - s is the reflection symmetry
   
   L4_r:
       X X
         X
         X
   
   L4_rr:
           X
       X X X
   
   L4_rrr:
       X 
       X  
       X X
   
   L4_s:
       X   
       X X X
   
   L4_rs (we apply s and then r):
       X X
       X  
       X  
   
   L4_rrs:
       X X X
           X
   
   L4_rrrs:
         X
         X
       X X
   
   Some polyomino only have one representation:
   For example, polyomino O has only one representation O_c 
   poly = [(0, 0), (0, 1), (1, 0), (1, 1)]
   
   O_c:
       X X
       X X
       
    We define the class Piece to manage any individual piece of the game,
   comprising:
   - name of the piece,
   - canonical representation,
   - other representations,
   - etc.
'''

################################################################
# Generating canonical form and all forms of a given polyomino #
################################################################
def minima(poly):
    '''
       Finds the min x and y coordinate of a polyomino.
       
       Note that pieces are translated to get minima(poly) == (0, 0)
       Example:
           poly = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)] # polyomino called X
           minima(poly) # (0, 0)
    '''
    return (min(pt[0] for pt in poly), min(pt[1] for pt in poly))
# # Explanation of the function:
# poly = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]
# # A representation of this poly:
# #   .X.
# #   XXX
# #   .X.
# # The upper-left corner is (0, 0)
# minima(poly) # (0, 0)

def maxima(poly):
    '''Finds the max x and y coordinate of a polyomino.
    
    Example:
        poly = [(0, 0), (0, 1), (0, 2), (1, 0)] # polyomino called L4
        maxima(poly) # (1, 2)
    '''
    return (max(pt[0] for pt in poly), max(pt[1] for pt in poly))
# # Explanation of the function:
# poly = [(0, 0), (0, 1), (0, 2), (1, 0)]
# # A representation of this poly:
# #   XXX
# #   X..
# # The bottom-right corner is (1, 2)
# maxima(poly) # (1, 2)
    
def text_representation(poly, char = '#'):
    '''Generates a textual representation of a polyomino.'''
    # text_representation_with_corners() outperforms text_representation(),
    # but we keep it for easier understanding of the code
    min_pt = minima(poly)
    max_pt = maxima(poly)
    table = [[' '] * (max_pt[1] - min_pt[1] + 1)
             for _ in range(max_pt[0] - min_pt[0] + 1)]
    for pt in poly:
        table[pt[0] - min_pt[0]][pt[1] - min_pt[1]] = char
    return('\n'.join([''.join(row) for row in table]))
# # Examples
# poly1 = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]
# poly2 = [(0, 0), (0, 1), (0, 2), (1, 0)]
# poly3 = [(0, 0), (0, 1), (1, 0), (1, 1)]
# print(text_representation(poly1))
# print(text_representation(poly2))
# print(text_representation(poly3))

def translate_to_origin(poly):
    '''Translates a polyomino such that minima(poly) == (0, 0).'''
    (minx, miny) = minima(poly)
    return [(x - minx, y - miny) for (x, y) in poly]
# Example:
# poly_ok = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]
# poly_to_translate = [(1, 0), (2, -1), (2, 0), (2, 1), (3, 0)]
# translate_to_origin(poly_to_translate) == poly_ok
 
def rotate90(xy):
    '''Rotates 90 degrees to the right'''
    x, y = xy
    return((y, -x))
    
def rotate180(xy):
    '''Rotates 180 degrees'''
    x, y = xy
    return((-x, -y))
   
def rotate270(xy):
    '''Rotates 270 degrees to the right'''
    x, y = xy
    return((-y,  x))
    
def reflect(xy):
    '''Reflection'''
    x, y = xy
    return((-x,  y))

def rotations_and_reflections(poly):
    '''All the plane symmetries of a rectangular region.'''
    symm_polys = [poly, 
                  [rotate90(pt) for pt in poly],
                  [rotate180(pt) for pt in poly],
                  [rotate270(pt) for pt in poly],
                  [reflect(pt) for pt in poly],
                  [rotate90(reflect(pt)) for pt in poly],
                  [rotate180(reflect(pt)) for pt in poly],
                  [rotate270(reflect(pt)) for pt in poly]]
    symm_polys = [sorted(translate_to_origin(pl)) for pl in symm_polys]
    return(symm_polys)
# # Example with 8 distinct forms
# poly = [(0, 0), (0, 1), (0, 2), (1, 0)] # L4
# out = rotations_and_reflections(poly)
# [print(text_representation(o), '\n') for o in out]

# # Example with 1 form shown 8 times
# poly = [(0, 0), (0, 1), (1, 0), (1, 1)]
# out = rotations_and_reflections(poly)
# [print(text_representation(o), '\n') for o in out]

def canonical(poly):
    '''Get the canonical form of a given polyomino poly.'''
    return min(rotations_and_reflections(poly))
# Example with L4:
# canonical([(0, 2), (1, 0), (1, 1), (1, 2)]) == [(0, 0), (0, 1), (0, 2), (1, 0)]

def idx_non_duplicates(lst):
    ''' 
        Non duplicates index of a list (keeping it ordered)
        Inspired from f7 at https://www.peterbe.com/plog/uniqifiers-benchmark
        
        Example:
        idx_non_duplicates([1,4,6,4,3,1,1,7]) # [0, 1, 2, 4, 7]
    '''
    # Transform the list into tuple:
    tple = [tuple(i) for i in lst]
    
    # Get indexes:
    seen = set()
    seen_add = seen.add
    return [i for (i,x) in enumerate(tple) if not (x in seen or seen_add(x))]
# # Examples with polyomino L4:
# symm_polys = rotations_and_reflections([(0, 0), (0, 1), (0, 2), (1, 0)])
# idx_non_duplicates(symm_polys) # [0, 1, 2, 3, 4, 5, 6, 7]
# 
# # Examples with polyomino O:
# symm_polys = rotations_and_reflections([(0, 0), (0, 1), (1, 0), (1, 1)] )
# idx_non_duplicates(symm_polys) # [0]
    
def rotations_and_reflections_unique_dict(canonical_poly):
    '''All the unique plane symmetries of a rectangular region.
       Outputs an ordered dict.
       Input must be the canonical form of a given polyomino, obtained using
       canonical(poly).
    '''
    move_names = ["c", "r", "rr", "rrr", "s", "rs", "rrs", "rrrs"]
    symm_polys = rotations_and_reflections(canonical_poly)
    idx = idx_non_duplicates(symm_polys)
    # {move_names[i]: symm_polys[i] for i in idx}
    output = OrderedDict([(move_names[i], symm_polys[i]) for i in idx])
    return(output)
# # Examples:
# canonical_poly = [(0, 0), (0, 1), (0, 2), (1, 0)] # L4
# rotations_and_reflections_unique_dict(canonical_poly)
# canonical_poly = [(0, 0), (0, 1), (1, 0), (1, 1)] # O
# rotations_and_reflections_unique_dict(canonical_poly)

############################################################
# Generating all canonical polyominos given a certain rank #
############################################################
def concat_map(func, it):
    '''
       Apply a mapping then flatten the resulting nested list
    
       Example:
           func = lambda x: [x, -x]
           it = range(2)
           concat_map(func, it) # [0, 0, 1, -1]
    '''
    return list(chain.from_iterable(map(func, it)))
# # Explanation of the function:
# # 1/ chain.from_iterable used to flatten a nested list:
# l = [[0], [1, 2], [2], [3, 6], [4], [5, 10]]
# list(chain.from_iterable(l)) # [0, 1, 2, 2, 3, 6, 4, 5, 10]
# # 2/ map apply function func on each element of iterable it
# list(map(lambda x: [x, -x], range(2))) # [[0, 0], [1, -1]]
# # 3/ Combined, we obtain:
# concat_map(lambda x: [x, -x], range(2)) # [0, 0, 1, -1]

def unique(lst):
    ''' Return unique elements of a list'''
    return(list(lst[k] for k in idx_non_duplicates(lst)))
# Example:
symm_polys = rotations_and_reflections([(0, 0), (0, 1), (0, 2), (1, 0)]) # L4
unique(symm_polys) # 8 elements, each a representation of L4
symm_polys = rotations_and_reflections([(0, 0), (0, 1), (1, 0), (1, 1)]) # O
unique(symm_polys) # Only 1 element: [[(0, 0), (0, 1), (1, 0), (1, 1)]]

def contiguous(xy):
    '''All four points in Von Neumann neighborhood.'''
    x, y = xy
    return([(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)])

def border(poly):
    '''Finds all points at the border of a polyomino (without corners).
       Those points can be added to a polyomino to increase its rank'''
    return unique([pt for pt in concat_map(contiguous, poly) if pt not in poly])
# # Example 1
# poly = [(0, 0), (0, 1), (0, 2), (1, 0)] # L4
# sorted(border(poly)) 
# # [(-1, 0), (-1, 1), (-1, 2), (0, -1), (0, 3), (1, -1), (1, 1), (1, 2), (2, 0)]
# # represented with '*' on the following representation:
# #    * * *
# #  * O O O *
# #  * O * *
# #    *
# 
# # Example 2
# poly = [(0, 0), (0, 1), (1, 0), (1, 1)] # O
# sorted(border(poly)) 
# # [(-1, 0), (-1, 1), (0, -1), (0, 2), (1, -1), (1, 2), (2, 0), (2, 1)]
# # represented with '*' on the following representation:
# #    * *
# #  * O O *
# #  * O O *
# #    * *

def new_polys(poly):
    ''' Adds all possible border to polyomino poly.'''
    return unique([canonical(poly + [pt]) for pt in border(poly)])
# # Example 1
# poly = [(0, 0), (0, 1), (0, 2), (1, 0)] # L4
# ([print(text_representation(i), '\n') for i in new_polys(poly)])
# # Example 2
# poly = [(0, 0), (0, 1), (1, 0), (1, 1)] # O
# ([print(text_representation(i), '\n') for i in new_polys(poly)])

def monominoe():
    ''' Initialize polyominos with monominoe.'''
    monomino = [(0, 0)]
    return(monomino)

def rank_fun(n):
    '''Generates polyominoes of rank n recursively.'''
    assert n >= 0
    if n == 0: return []
    if n == 1: return [monominoe()]
    return sorted(unique(concat_map(new_polys, rank_fun(n - 1))))
# Test cases:
# print([len(rank(n)) for n in range(1, 11)]) 
# # [1, 1, 2, 5, 12, 35, 108, 369, 1285, 4655] as expected at http://oeis.org/A000105
#
# ([print(text_representation(i), '\n') for i in rank(1)])
# ([print(text_representation(i), '\n') for i in rank(2)])
# ([print(text_representation(i), '\n') for i in rank(3)])
# ([print(text_representation(i), '\n') for i in rank(4)])
# ([print(text_representation(i), '\n') for i in rank(5)])

#####################
# Polyomino corners #
#####################
def diagonal(xy):
    '''All four points in the diagonal.'''
    x, y = xy
    return([(x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)])

def corners(poly):
    '''Finds all points at the corner of a polyomino (without border)'''
    candidates = unique([pt for pt in concat_map(diagonal, poly) if pt not in poly])   
    
    def is_corner(candidate, poly):
        '''Check whether candidate is a corner or not (outputs a boolean)'''
        # [i for i in contiguous(candidate) if i in poly] is the list of 
        # contiguous elements of the candidate which are in the initial poly.
        # If any element is like this (i.e. non empty list), then the candidate
        # is not a corner.
        # If the list is empty, the candidate is a corner.
        return(not [i for i in contiguous(candidate) if i in poly])
    
    # https://stackoverflow.com/questions/18665873/filtering-a-list-based-on-a-list-of-booleans
    fil = [is_corner(candidate, poly) for candidate in candidates]
    corner_out = list(compress(candidates, fil))
    return(sorted(corner_out))
    
# # Example 1
# poly = [(0, 0), (0, 1), (0, 2), (1, 0)] # L4
# corners(poly)
# # [(-1, -1), (-1, 3), (1, 3), (2, -1), (2, 1)]
# # represented with '*' on the following representation:
# #  *       *
# #    O O O
# #    O     *
# #  *   *
# 
# # Example 2
# poly = [(0, 0), (0, 1), (1, 0), (1, 1)] # O
# corners(poly)
# # [(-1, -1), (-1, 2), (2, -1), (2, 2)]
# # represented with '*' on the following representation:
# #  *     *
# #    O O 
# #    O O 
# #  *     *

def text_representation_with_corners(poly, char = '#', char_corners = '*'):
    '''Generates a textual representation of a polyomino with its corners.'''
    poly_corners = corners(poly)
    min_pt = minima(poly_corners)
    max_pt = maxima(poly_corners)
    table = [[' '] * (max_pt[1] - min_pt[1] + 1)
             for _ in range(max_pt[0] - min_pt[0] + 1)]
    for pt in poly:
        table[pt[0] - min_pt[0]][pt[1] - min_pt[1]] = char
    for pt in poly_corners:
        table[pt[0] - min_pt[0]][pt[1] - min_pt[1]] = char_corners
    return('\n'.join([''.join(row) for row in table]))
# # Example 1
# poly = [(0, 0), (0, 1), (0, 2), (1, 0)] # L4
# print(text_representation_with_corners(poly))
#
# # Example 2
# poly = [(0, 0), (0, 1), (1, 0), (1, 1)] # O
# print(text_representation_with_corners(poly))
    
###############
# Class Piece #
###############
class Piece(list):
    def __init__(self, my_list = monominoe(), name = None, color = None):
        # Default name if non existant
        if name is None:
            name = str(my_list)
            
        # Initialize with the canonical version of the piece
        canonical_args = canonical(my_list)        
        list.__init__(self, canonical_args)
        
        # Ordered dictionary of symmetries of the piece
        self.forms = rotations_and_reflections_unique_dict(canonical_args)

        # Name of the piece
        self.name = name
        
        # Color of the piece
        self.color = color
        
    def text_repr(self):
        ''' Give a visual representation as a matrix of the piece'''
        print(text_representation_with_corners(self, '#', ' '))
        return(None)
        
    def summary(self, with_corners = True):
        ''' Give a visual representation of all representations of the piece
            with names'''
        print('*** Piece', self.name, '***')
        for key, poly in self.forms.items():
            print('<', key, '>')
            char_corners = '*'
            if not with_corners:
                char_corners = ' '
            print(text_representation_with_corners(poly, '#', char_corners), '\n')
        return(None)
        
    def size(self):
        ''' Give size of the canonical represention of the piece, 
            with index begining at 0'''
        return(maxima(self))
        
    def nb_of_repr(self):
        ''' Give number of representation of the piece, between 1 and 8.'''
        return(len(self.forms))
        
# # Example
# my_piece = Piece([(3, -1), (3, 0), (4, 0), (4, 1)], 'Z4')
# my_piece.text_repr()
# my_piece.summary()
# my_piece.summary(with_corners = False)
# my_piece.size()
# my_piece.nb_of_repr()
# my_piece.forms['r']
# corners(my_piece.forms['r'])

#####################
# Class BagOfPieces #
#####################
class BagOfPieces(list):
    def __init__(self, color = 'blue', player = 0, max_rank = 5):
        '''Define a colored bag of pieces assigned to a specific player'''
        self.color = color
        self.player = player
        self.max_rank = max_rank
        
        self.pieces = []
        names = dict()
        names[1] = ['1']
        names[2] = ['2']
        names[3] = ['I3', 'V3']
        names[4] = ['I4', 'L4', 'T4', 'O', 'Z4']
        names[5] = ['I5', 'L5', 'Y', 'P', 'U', 'V5', 'T5', 'N', 'F', 'W', 'Z5', 'X']
        for r in range(1, max_rank+1):
            try:
                names_r = names[r]
            except KeyError:
                names_r = None
            to_add = [Piece(poly, name, color) for poly, name in zip(rank_fun(r), names_r)]
            self.pieces.append(to_add)
        self.pieces = list(chain.from_iterable(self.pieces))
        
        list.__init__(self, self.pieces)

# Example
# bag = BagOfPieces(color = 'blue', player = 0)
