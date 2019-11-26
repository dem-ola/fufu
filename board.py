import constants as C 	# constants' namespace
import numpy as np

def create_board():
    ''' create game board and fill with blanks '''
    shape = C.board_shape
    board = np.empty((shape,shape), dtype='object')
    board[:] = ''
    return board