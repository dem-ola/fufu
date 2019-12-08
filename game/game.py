#!/usr/bin/python3

import os, sys, re, json, random
from collections import defaultdict
from itertools import dropwhile
import valid
import constants as C 	# constants' namespace
from board import create_board, update_board, board_shape
from fus import Fu, fus, STATIC_SQUARE
from weapons import Weapon, weapons
from fuencoder import GameEncoder
from fight import fight
from moves import get_moves, deltas
from outputs import print_update, final_state

# current file directory
file_dir = os.path.dirname(os.path.abspath(__file__))

board = None
fu_dict		= {}	# store players
weap_dict 	= {}	# store weapons
static_square = STATIC_SQUARE
occupied	= defaultdict(list)	# occupied squares and occupiers
weaponised	= defaultdict(list)	# squares with free weapons

numpy_ = True
import numpy as np
if numpy_:
	try:
		import numpy as np		# for array to display board
	except:
		numpy_ = False

def load_fus():
	''' create fus and store them in dictionary '''
	global board
	for f in (Fu(name, position) for name, position, rgb in fus):
		fu_dict[f.alpha] = f
		occupied[f.position].append(f)

		# player in static squares picks up weapon 
		if f.static:
			wp = weapons_here(f.position)
			f.pick_weapon(wp)
			del weaponised[static_square]	
		board = update_board(board, fu_dict, 'Fu', f, f.position, 'new')

def load_weapons():
	''' create weapons and store them in dictionary '''
	global board
	for wp in (Weapon(name, position) for name, position in weapons):
		weap_dict[wp.alpha] = wp
		weaponised[wp.position].append(wp)
		board = update_board(board, fu_dict, 'weapon', wp, wp.position, 'new')

def weapons_here(move_to):
	''' gets any free weapons on a square '''
	weaps = [weaponised[w] for w in weaponised if w == move_to]
	return weaps[0] if weaps else None

def fus_here(move_to):
	''' gets any still alive Fu on square '''
	kn = [occupied[k] for k in occupied if k == move_to]
	if kn: #nb. this is a list in a list
		kn = list(dropwhile(lambda k: not k.alive, kn[0]))
	return kn[0] if kn else None

def update_occupied(fu):
	''' update dictionary tracking occupied squares '''
	# remove entry in old position ; delete old if empty
	# create new entry with new position
	last_pos = fu.last_position
	occupied[last_pos].remove(fu)
	if not occupied[last_pos]:
		del occupied[last_pos]
	occupied[fu.position].append(fu)	

def update_weaponised(weapon):
	''' add weapon to dict if no owner else remove '''	
	wp_pos = weapon.position
	if weapon.owner is None:
		weaponised[wp_pos].append(weapon)
	else:
		if wp_pos in weaponised:
			if weapon in weaponised[wp_pos]:
				if len(weaponised[wp_pos]) == 1:
					del weaponised[wp_pos]
				else:
					weaponised[wp_pos].remove(weapon)

def play():
	''' get down and play '''
	
	global board
	m = 0
	for move in get_moves():

		m += 1
		pre_occupied = False

		# get Fu and direction
		kn, rxn = move.split(valid.SEP)
		k = fu_dict[kn]

		# we only care about fus still on board
		if k.alive:

			# static player does not move
			if k.static: continue

			print('\n',f'{m}:',k.alpha,'->',rxn)
			
			# figure out where to move to
			delta = deltas[rxn]
			move_to = tuple([(i+j) for i,j in zip(k.position, delta)])

			# flag if already occupied - do this before calling shift
			occupier = fus_here(move_to)
			if occupier is not None:
				pre_occupied = True
				print('occupied by',occupier)
			
			# move and update occupied
			# shift returns weapon - in case after move
			# an item was picked up - we can then update weaponised
			k_weapon = k.shift(move_to, weapons_here(move_to))
			update_occupied(k)
			if k_weapon is not None:
				update_weaponised(k_weapon)

			# update game board
			# if drowning, FU throws weapon back and goes offboard
			# we show that here, not inside the class
			# for fus: remove from old position, add to new
			if Fu.offboard(move_to): 
				last_wp = k.last_weapon
				if last_wp is not None:
					board = update_board(board, fu_dict,
						'weapon', last_wp, last_wp.position, 'throw')
			board = update_board(board, fu_dict, 'Fu', k, k.last_position, 'old')
			board = update_board(board, fu_dict,'Fu', k, k.position, 'new')
			print_update(board=board, fu_dict=fu_dict, weap_dict=weap_dict, 
							occupied=occupied, weaponised=weaponised)		
				
			# no further action except if two fus meet
			# since two's a crowd, they fight
			if pre_occupied:

				# get scores before battle
				a_bat = (k.attack, k.defence, k.weapon.score if k.weapon else 'None')
				d_bat = (occupier.attack, occupier.defence, occupier.weapon.score if occupier.weapon else 'None')
				
				# fight
				winner, loser = fight(k, occupier)	

				# add loser's weapon (if any) back to free list in dict
				loser.dying()
				last_wp = loser.last_weapon
				if last_wp is not None:
					update_weaponised(loser.last_weapon)

					# if winner has no weapon then pick the weapon
					if winner.weapon is None:
						winner.pick_weapon([loser.last_weapon])
						update_weaponised(winner.weapon)
				
				# update board - will also handle weapon
				board = update_board(board, fu_dict, 'Fu', loser, loser.position, 'dead')
				board, update_board(board, fu_dict, 'Fu', winner, winner.position, 'old')
				board, update_board(board, fu_dict, 'Fu', winner, winner.position, 'new')
				print_update(board=board, fu_dict=fu_dict, weap_dict=weap_dict, 
							occupied=occupied, weaponised=weaponised,
							a_bat=a_bat, d_bat=d_bat, battle=(k, occupier, winner, loser))

	
def main():
	''' main thread - load and play '''

	if numpy_:
		global board
		board = create_board(board_shape)	# numpy array

	load_weapons()	# from constants
	load_fus()	# from constants
	
	print('= LOAD GAME =\n')
	print_update(board=board, fu_dict=fu_dict, weap_dict=weap_dict, 
							occupied=occupied, weaponised=weaponised)	# show start position

	play()			# play
	final_state(fu_dict=fu_dict, weap_dict=weap_dict)	# write final state to json


# --------------------------------------------------------------

if __name__ == '__main__':
	
	args = sys.argv

	# don't load NumPy if not needed 
	if '-numpy' in args: numpy_ = False
	
	# run randmoves.py if called
	if 'rand' in args:
		rid = args.index('rand')
		import randmoves
		try:
			set_moves = int(args[rid+1])
			randmoves.main(set_moves)
		except:
			randmoves.main()

	# run script
	main()
	
