# -*- coding: utf-8 -*-

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

#from modules.piece import BagOfPieces
from piece import BagOfPieces


###############
# Class Board #	   # A very ongoing version of python class for blokus board
###############

def define_color2player() :
    '''Allows manual assignment of each color to a player. Colors can be discarted, 
       and a same player can play several colors.
    '''
    Sortie = {}
    colors = ['blue', 'yellow', 'red', 'green']
    for color in colors :
        player = input('player number for color {} (integer between 1 and 4, or 0 if color discarted) : '.format(color))
        try :
            Sortie[color] = int(player)
        except KeyError as e:
            print(e)
    return Sortie
# # Ex :
# color2player = define_color2player()
# color2player

color2player = define_color2player()
print(color2player)



class Board:
    '''The state of a game consists of a collection of colors with associated player, with for each color :
    
        - A bag of available pieces of this color, stored in self.bags
        - The space already filled by this color on the board, stored in self.occupancies
        
    '''
    # ------------ initialization -------------
    def __init__(self, color2player, board_size = 20, max_rank = 5):
        
        # define main content of a board, that is, for each color to be played :
        #      - bag of remaining pieces 
        #      - positions of already placed pieces
        self.colors = []
        self.bags = {}
        self.occupancies = {}
        
        # initialize bag of pieces and occupied zone for each color to be played
        for color, player in color2player.items():
            if player != 0 :
                self.colors.append(color)
                self.bags[color] = BagOfPieces(color, player, max_rank)
                self.occupancies[color] = np.zeros((board_size, board_size))
        
        # keep relevant quantities
        self.board_size = board_size
        self.to_play = self.colors[0] # current player, initialized at first color to be played
        
        #self.color2player = color2player
        #self.players = color2player.values()
    
    
    # -------------- interface ----------------
    def show(self):
        '''Shows the board filled with played pieces'''
        # performs weighted sum of occupancy matrices
        vals = sum([self.occupancies[color] * 2*(int(i)+1) for i, color in enumerate(self.occupancies)])
        
        # define thresholds for colormap
        cmap = mpl.colors.ListedColormap(['white'] + list(self.colors))
        bounds = [ 2*int(i)+1 for i in range(-1, len(self.colors)+1)]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        
        # define matplotlib img  
        fig, ax = plt.subplots()
        img = ax.imshow(vals, interpolation='nearest', cmap=cmap, norm=norm)
        
        # add grid
        ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=1)
        ax.set_xticks([i for i in range(self.board_size +1)])
        ax.set_yticks([i for i in range(self.board_size +1)])
        #img = plt.imshow(vals, cmap = cmap, norm=norm)
        
        # display colors to be played
        plt.colorbar(img, cmap=cmap, norm=norm, boundaries=bounds, ticks = [])# [2*int(i) for i in range(len(self.colors)+1)] )
        
        plt.show()

        
    def show_available_pieces(self, color):
        '''Prints the remaining available pieces of a given color.'''
        bag = self.bags[color]
        for piece in bag.pieces :
            piece.text_repr()
        return
        
    
    # --------- internal state of game -----------    
    def is_allowed(self, color, piece_name, orientation, position) :
        '''Returns True whether the given piece at the given orientation and given position
           on the board fits to the current state of the game, else returns False.
        '''
        bag = self.bags[color]
        played_piece = bag.selectPiece(piece_name)
        surface_np =  np.array(played_piece.forms[orientation]) + np.array(position)
        surface = [tuple(pt) for pt in surface_np]
        
        # 1) tests whether piece fits on the board
        if  minima(surface)[0] < 0 or \
            minima(surface)[1] < 0 or \
            maxima(surface)[0] > self.board_size or \
            maxima(surface)[1] > self.board_size :
                return False
        
        # 2) if game starts, piece must cover the board angle corresponding to current color to play
        if len(bag) == 21 :
            # TODO
            return
            
        # 3) piece must not cross already occupied positions on board
        # TODO
        
        # 4) boundary(piece) must cross positions already occupied by the given color
        # TODO
        
        #if all true, returns True
        return True


    def scores(self, last_piece_name = None):
        '''Computes the cumulated negative reward from remaining pieces for each color.
           Last_piece_name is passed in argument only when game is over after this piece was played'''
        scores = {}
        for color in self.colors :
            scores[color] = sum([len(piece) for piece in self.bags[color]]) # malus function is len()
            if scores[color] == 0 and last_piece_name == '1' :
                scores[color] += 20
            elif scores[color] == 0 :
                scores[color] += 15
        return scores
        
    
    def is_end(self):
        '''Returns True if game is over, else False.'''
        #TODO
        return
    
    
    def init_board(self) :
        for color in self.colors :
            self.occupancies[color] = np.zeros((self.board_size, self.board_size))
    
    
    # ------------- update methods -----------------
    def remove_piece_from_bag(self, piece_name):
        '''Remove a piece from current color's bag.'''
        bag = self.bags[self.to_play]
        played_piece = bag.selectPieceByName(piece_name)
        bag.pieces.remove(played_piece) # or bag.remove(played_piece)
        return
    
                          
    def put_piece_on_board(self, color, piece_name, orientation, position):
        '''Puts on board the piece with given name and orientation at the 
           given position.
        '''
        bag = self.bags[color]                                                   # select bag of pieces
        played_piece = bag.selectPiece(piece_name)                               # select piece
        surface = np.array(played_piece.forms[orientation]) + np.array(position) # the list of 2D points on the board occupied by the piece
        for pt in surface : 
            self.occupancies[color][tuple(pt)] = 1                               # board update
        return
    
                          
    def update_player(self):
        '''Move from a color to the next in the set of colors assigned to a game, 
           with colors ordered as : 'blue', 'yellow', 'red', 'green'.
        '''
        for i, color in enumerate(self.colors) :
            if self.to_play == color:
                j = i+1 % len(self.colors)
                self.to_play = self.colors[j]
                return
        
    
    # ------------- perform a move -----------------
    def apply_move(self, color, piece_name, orientation, position) :
        self.remove_piece_from_bag(piece_name)
        self.put_piece_on_board(color, piece_name, orientation, position)
        self.update_player()
        return
    
    
    def forward(self):
        # 1) dysplaying available pieces and orientations to current player
        self.show_available_pieces(self.to_play)
        
        done = False
        while done == False :
            # 2) retrieve playing act
            # TODO
            #piece, orientation, position = input('which action ?')
            
            # 3) either update game state or raise error
            if self.is_allowed(self.to_play, piece_name, orientation, position) :
                self.apply_move(self.to_play, piece_name, orientation, position)
                done = True
            else :
                #raise error 
                print('invalid action')
                
            # 4) if end of game print scores
            if self.is_end() :
                scores = self.scores(last_piece_name = piece_name)
                print(scores)
                
   
                
   
    


    
# # Ex :
board = Board(color2player, board_size = 10)
print(board.colors)
print(board.to_play)
print(board.occupancies[board.to_play])
board.show_available_pieces(board.to_play)

board.init_board()
board.put_piece_on_board(color = board.to_play, piece_name = 'V5', orientation = 'rr', position = (5, 5))
board.update_player()
board.put_piece_on_board(color = board.to_play, piece_name = '2', orientation = 'r', position = (2,1))
board.update_player()
board.put_piece_on_board(color = board.to_play, piece_name = 'X', orientation = 'c', position = (5,3))
board.show()
