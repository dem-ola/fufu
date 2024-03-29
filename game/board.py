import re
import numpy as np

board_shape	= 13

def create_board(shape=board_shape):
    ''' create game board and fill with blanks '''
    board = np.empty((shape,shape), dtype='object')
    board[:] = ''
    return board

def update_board(board, fus, piece, elem, position, state):
    ''' update board position 

		piece: 'Fu' or 'weapon' string
		elem: fu or weapon instance
		position: (y, x) coordinates
		state: 'old' coords, 'new' coords or 'dead' Fu
	'''
    
    # check if offboard as board access error
	# if position goes off axis south (8, _)
	# or off axis east (_, 8)
    offboard = True if position == 'null' else False
	
	# current board entry at position
    current = None if offboard else board[position]

	# leading alpha character
    name = elem.alpha

	# interim storage of string before updating position
    updated = ''
	
	# empty squares
    if current == '':
        if piece == 'Fu':

			# nothing to update if dead or drowned
            if not elem.alive:
                name = ''
			
			# show name plus weapon if any
            else:
                wp = elem.weapon
                if wp is not None:
                    name += '->' + wp.alpha
                else:
                    name += '->0' # indicates no weapon held
		
        updated = name

	# non-empty square or going offboard/drowning
    else:
        if piece == 'Fu':

			# usually two request calls are made
			# 1. scrub from old place on board
			# 2. write to new place on board

			# scrub Fu from old position 
            if state == 'old':
                current = re.sub(r'/?'+name+r'.*?[0,A-Z]', '', current)
                updated = current
			
			# write new position linking weapon to Fu
			# remove from 'free' list any weapon picked up 
			# don't bother writing if Fu going offboard
            else:
                if not offboard:
					
					# DEAD Fus stay onboard; we'll reconstruct the string
					# scrub old, move last weapon held to front
					# add 'x' to name as visual cue
                    if not elem.alive:
                        current = re.sub(r'/?'+name+r'.*?[0,A-Z]', '', current)

                        if elem.last_weapon is not None:
                            if current[0] in fus.keys():
								# add slash if first item is a Fu
								# e.g. H/Gx->0/R->A/Bx->0
                                current = \
									elem.last_weapon.alpha + '/' + current
                            else:
								# first item is a weapon, skip slash
								# e.g. MH/Gx->0/R->A/Bx->0
                                current = elem.last_weapon.alpha + current
                        name += 'x'

					# for weapon links: if no weapon or dead then use '0'
					# aiming for a format: K->W, also H/K->W/K->W
                    wp_name = elem.weapon.alpha if elem.weapon else '0'
					
                    if wp_name != '0':
                        current = current.replace(wp_name, '').strip('/')	
	
                    slash = '/' if len(current) > 0 else ''
                    name += '->' + wp_name
                    updated = current + slash + name

		# applies if there's already a weapon on the square
		# or if more than one weapon loaded on square
		# or weapon thrown back by drowning Fu -> A/Rx->0[drowned:G->A]
		# add at start to align with print format
        else:
            if board[position][0] in fus.keys():
                updated = name + '/' + board[position]
            else:
                updated = name + board[position]

	# clean and update board
    if not offboard:
        board[position] = updated.strip('/')
        
    return board
