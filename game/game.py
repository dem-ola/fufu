#!/usr/bin/python3

import sys, re, json, random
import valid
from board import create_board, update_board
from fus import Fu, fus
from weapons import Weapon, weapons
from encoder import GameEncoder

import constants as C 	# constants' namespace
from collections import defaultdict
from operator import attrgetter
from itertools import dropwhile

board = None
fu_dict		= {}	# store players
weap_dict 	= {}	# store weapons
static_player = None
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
	global static_player, board
	for f in (Fu(name, position) for name, position, rgb in fus):
		fu_dict[f.alpha] = f
		occupied[f.position].append(f)

		# player in static squares picks up weapon 
		if f.position == C.static_square:
			wp = weapons_here(f.position)
			f.pick_weapon(wp)
			static_player = f
			del weaponised[C.static_square]	
		board = update_board(board, fu_dict, 'knight', f, f.position, 'new')

def load_weapons():
	''' create weapons and store them in dictionary '''
	global board
	for wp in (Weapon(name, position) for name, position in weapons):
		weap_dict[wp.alpha] = wp
		weaponised[wp.position].append(wp)
		board = update_board(board, fu_dict, 'weapon', wp, wp.position, 'new')

def get_moves():
	''' get next move from file '''
	with open(C._FILE) as f:
		if not valid.valid_file(f): # kill + warn if invalid file
			raise Exception('Please use a valid game file')
		else:
			f.seek(0)
			while True:
				line = f.readline().strip()
				if line == C._END:	# at end of file
					break
				if line not in [C._START, '']: # skip first line, blanks
					yield line

def weapons_here(move_to):
	''' gets any free weapons on a square '''
	weaps = [weaponised[w] for w in weaponised if w == move_to]
	return weaps[0] if weaps else None

def fus_here(move_to):
	''' gets any still alive knight on square '''
	kn = [occupied[k] for k in occupied if k == move_to]
	if kn: #nb. this is a list in a list
		kn = list(dropwhile(lambda k: not k.alive, kn[0]))
	return kn[0] if kn else None

def update_occupied(knight):
	''' update dictionary tracking occupied squares '''
	# remove entry in old position ; delete old if empty
	# create new entry with new position
	last_pos = knight.last_position
	occupied[last_pos].remove(knight)
	if not occupied[last_pos]:
		del occupied[last_pos]
	occupied[knight.position].append(knight)	

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

def fight(challenger, defender):
	''' determine fight winner based on higer score '''

	c_score = challenger.attack + \
				challenger.defence * 0.5 + \
					(challenger.weapon.score if challenger.weapon else 0)

	d_score = 0
	if defender == static_player:
		d_score = defender.defence + defender.weapon.score
	else:
		d_score = defender.defence + \
					defender.attack * 0.5 + \
					(defender.weapon.score if defender.weapon else 0)

	challenger.battle_score = c_score
	defender.battle_score = d_score

	#  declare winner/loser
	# winners get a bonus
	# they also get weapons rescored
	# as weapons could be damaged/enhanced during fight

	if c_score > d_score:
		winner = challenger
		challenger.attack += C._WIN_BONUS
		if challenger.weapon is not None: challenger.weapon.rescore()
		loser = defender
	else: # including draws - here defender considered winner
		loser = challenger
		winner = defender
		defender.defence += C._WIN_BONUS
		if defender.weapon is not None: defender.weapon.rescore()

	return winner, loser

def play():
	''' get down and play '''
	
	global board
	m = 0
	for move in get_moves():

		m += 1
		pre_occupied = False

		# get knight and direction
		kn, rxn = move.split(C._SEP)
		k = fu_dict[kn]

		# we only care about fus still on board
		if k.alive:

			# static player does not move
			if k == static_player: continue

			print('\n',f'{m}:',k.alpha,'->',rxn)
			
			# figure out where to move to
			delta = C.deltas[rxn]
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
			# if drowning, knight throws weapon back and goes offboard
			# we show that here, not inside the class
			# for fus: remove from old position, add to new
			if Fu.offboard(move_to): 
				last_wp = k.last_weapon
				if last_wp is not None:
					board = update_board(board, fu_dict,
						'weapon', last_wp, last_wp.position, 'throw')
			board = update_board(board, fu_dict, 'knight', k, k.last_position, 'old')
			board = update_board(board, fu_dict,'knight', k, k.position, 'new')
			print_update()		
				
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

					# rules unclear if knight with no weapon
					# arrives on tile with no free weapons but still
					# defeats a defending knight with weapon
					# the dead knight drops their weapon
					# here we'll do the obvious thing: pick the weapon
					if winner.weapon is None:
						winner.pick_weapon([loser.last_weapon])
						update_weaponised(winner.weapon)
				
				# update board - will also handle weapon
				board = update_board(board, fu_dict, 'knight', loser, loser.position, 'dead')
				board, update_board(board, fu_dict, 'knight', winner, winner.position, 'old')
				board, update_board(board, fu_dict, 'knight', winner, winner.position, 'new')
				print_update(a_bat, d_bat, battle=(k, occupier, winner, loser))


def print_update(a_bat=None, d_bat=None, battle=False):

	if battle:
		attacker, defender, winner, loser = battle
		print()
		print('BATTLE!', attacker, a_bat, 'attacks', defender, d_bat)
		print('Winner', winner, winner.battle_score)
		print('Loser', loser, loser.battle_score)
		last_wp = loser.last_weapon
		if last_wp:
			print(loser, 'drops weapon ->', last_wp)
			if last_wp == winner.weapon:
				print(winner, 'picks up ->', winner.weapon)

	if numpy_: print(board)
	Fs = []
	for f in fu_dict:
		f_ = fu_dict[f]
		Fs.append((f_, f_.attack, f_.defence, f_.weapon.score if f_.weapon else 'None'))
	print('{:12}'.format('Scores'), Fs)
	print('{:12}'.format('Positions'), dict(occupied))
	print('{:12}'.format('Free Weapons'), dict(weaponised))

def final_state():
	''' dump json '''

	# create dictionary with fus and weapons
	jdict = {}
	
	for obj in fu_dict.values():
		item = obj.weapon
		item = item.name.lower() if item is not None else 'null' 
		jdict[obj.name.lower()] = \
			[obj.position, obj.status, item, obj.attack, obj.defence] 
	
	for obj in weap_dict.values():
		obj_owner = obj.owner
		jdict[obj.name.lower()] = \
			[obj.position, 
			obj_owner.name.lower() if obj_owner is not None else False]

	# create a json string to display - note: custom encoder
	json_ = json.dumps(jdict, indent=2, cls=GameEncoder)
	print()
	print(json_)

	# write to file - note: custom encoder
	with open('final_state.json', 'w') as jf:
		json.dump(jdict, jf, indent=2, cls=GameEncoder)

	
def main():
	''' main thread - load and play '''

	if numpy_:
		global board
		board = create_board(C.board_shape)	# numpy array

	load_weapons()	# from constants
	load_fus()	# from constants
	
	print('= LOAD GAME =\n')
	print_update()	# show start position

	play()			# play
	final_state()	# write final state to json


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
	
