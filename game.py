#!/usr/bin/python3

import sys, re, json, random

import constants as C 	# constants' namespace
from collections import defaultdict
from operator import attrgetter
from itertools import dropwhile

board 		= None	# game board
knights 	= {}	# store players
weapons 	= {}	# store weapons
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

def valid_file(f):
	''' checks if file is valid '''

	# check game start
	top = f.read(len(C._START))
	top_ = top.startswith(C._START)

	# check game end
	f.seek(0,2)              		# go to end of file
	f.seek(f.tell() - len(C._END))  # go backwards
	end = f.read()
	end_ = end.endswith(C._END)

	# check mid sections for proper syntax
	# we can choose not to do this and just skip invalid lines
	# but with large game input files this could be harder to debug
	# so we'll check all the lines upfront
	# blank lines will be skipped
	mid_ = True
	f.seek(0)		# move back to top of file
	for line in f:
		lenn = len(line.strip())
		if not line.startswith(C._FLAG) and lenn > 0:
			if lenn != 3 or \
				line[0] not in C.players_ or \
				line[1] != C._SEP or \
				line[2] not in C.directions:
				mid_ = False
				break

	return all((top_, end_, mid_))

def create_board():
	''' create game board and fill with blanks '''
	global board
	shape = C.board_shape
	board = np.empty((shape,shape), dtype='object')
	board[:] = ''

def update_board(piece, elem, position, state):
	''' update board position 

		piece: 'knight' or 'weapon' string
		elem: knight or weapon instance
		position: (y, x) coordinates
		state: 'old' coords, 'new' coords or 'dead' knight

	'''

	if not numpy_: return

	global board

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
		if piece == 'knight':

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
		if piece == 'knight':

			# usually two request calls are made
			# 1. scrub from old place on board
			# 2. write to new place on board

			# scrub knight from old position 
			if state == 'old':
				current = re.sub(r'/?'+name+r'.*?[0,A-Z]', '', current)
				updated = current
			
			# write new position linking weapon to knight
			# remove from 'free' list any weapon picked up 
			# don't bother writing if knight going offboard
			else:
				if not offboard:
					
					# DEAD knights stay onboard; we'll reconstruct the string
					# scrub old, move last weapon held to front
					# add 'x' to name as visual cue
					if not elem.alive:
						current = re.sub(r'/?'+name+r'.*?[0,A-Z]', '', current)

						if elem.last_weapon is not None:
							if current[0] in knights.keys():
								# add slash if first item is a knight
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
		# or weapon thrown back by drowning knight -> A/Rx->0[drowned:G->A]
		# add at start to align with print format
		else:
			if board[position][0] in knights.keys():
				updated = name + '/' + board[position]
			else:
				updated = name + board[position]

	# clean and update board
	if not offboard:
		board[position] = updated.strip('/')

class Knight():
	''' Knights i.e. players '''

	_static = C._STATIC_SKILL
	_static_sq = C.static_square

	def __init__(self, name, position):
		self.alpha = name[0]
		self.name = name
		self.position = position
		self.last_position = position
		self.alive = True
		self.status = 'LIVE'
		self.weapon = None
		self.last_weapon = None
		self.battle_score = 0 	# for printing winner/loser
		self.set_score()

	@staticmethod
	def offboard(move_to):
		''' check if new coordinates still on board '''
		if move_to == 'null':
			return True
		shape = C.board_shape - 1
		return any(i for i in move_to if i < 0 or i > shape)
		
	def set_score(self):
		if self.position == Knight._static_sq:
			attack = 0
			defence = Knight._static
		else:
			attack = random.randrange(
				C._FU_ATTACK_SKILL[0], C._FU_ATTACK_SKILL[1] + 1)
			defence = random.randrange(
				C._FU_DEFENCE_SKILL[0], C._FU_DEFENCE_SKILL[1] + 1)
		self.attack = attack
		self.defence = defence

	def pick_weapon(self, the_weapons):
		''' knight picks a weapon from square '''

		# only called when knight doesn't already have a weapon
		# and there are weapons freely available on the square
		# sort weapons by preference/rank and pick highest ranking

		if len(the_weapons) > 1:
			the_weapons.sort(reverse=True, key=attrgetter('rank'))
		picked = the_weapons[0]
		self.weapon = picked

		# update weapon attributes
		picked.owner = self
		picked.position = self.position

		return picked

	def kaput(self, status):
		''' stuff to do if drowning or dying '''
		self.last_weapon = self.weapon
		if self.weapon is not None: # as None cannot have .owner
			self.weapon.owner = None
		self.weapon = None
		self.alive = False
		self.status = status
		self.attack = 0
		self.defence = 0

	def shift(self, move_to=None, avail_weapons=None):
		''' move knight '''
	
		if self.alive and move_to is not None:

			picked = None	# for weapon
			
			# record old and new positions
			self.last_position = self.position
			self.position = move_to

			# stuff to do if drowning
			# knight throws weapon on bank at last position
			# thus reaches outside to update weaponised
			if self.offboard(move_to):
				# take before kaput - but update after when owner is None
				wp = self.weapon
				self.kaput('DROWNED')
				self.position = 'null'
				if wp is not None:
					update_weaponised(wp)

			# update weapon position if have weapon
			# if not, pick a free one if available
			else:
				if self.weapon is not None:
					self.weapon.position = move_to
				else:
					if avail_weapons is not None:
						picked = self.pick_weapon(avail_weapons)

			# prints
			self_pos = 'drowns' if self.position == 'null' else self.position
			print('moved:', self.last_position, '->', self_pos)
			if avail_weapons is not None: print('free weapons', avail_weapons)
			if picked is not None: print(self, 'picks ->', picked)

		return self.weapon

	def dying(self):
		''' stuff to do if dying - from battle '''
		self.kaput('DEAD')

	def __repr__(self):
		return self.alpha

class Weapon():
	''' Weapons '''

	def __init__(self, name, position):
		self.alpha = name[0]
		self.name = name
		self.position = position	# y,x tuple
		self.owner = None
		self.set_score()

	@property
	def rank(self):
		#plus random in case 2+ weapons with same score
		return self.score + random.random()

	def rescore(self):
		''' after each battle we do this for the winner
			because the weapon could be damaged or enhanced eg sharpened
			during battle '''
		self.set_score()

	def set_score(self):
		self.score = random.randrange(C._WP_SCORE[0], C._WP_SCORE[1] + 1)

	def __repr__(self):
		return self.alpha

def create_knights():
	''' create knights '''
	for name, position in C.knights:
		yield Knight(name, position)

def load_knights():
	''' create knights and store them in dictionary '''
	global static_player
	for kn in create_knights():
		knights[kn.alpha] = kn
		occupied[kn.position].append(kn)

		# player in static squares picks up weapon 
		if kn.position == C.static_square:
			wp = weapons_here(kn.position)
			kn.pick_weapon(wp)
			static_player = kn
			del weaponised[C.static_square]
		
		update_board('knight', kn, kn.position, 'new')

def create_weapons():
	''' create weapons '''
	for name, position in C.weapons:
		yield Weapon(name, position)

def load_weapons():
	''' create weapons and store them in dictionary '''
	for wp in create_weapons():
		weapons[wp.alpha] = wp
		weaponised[wp.position].append(wp)
		update_board('weapon', wp, wp.position, 'new')

def get_moves():
	''' get next move from file '''
	with open(C._FILE) as f:
		if not valid_file(f): # kill + warn if invalid file
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

def knights_here(move_to):
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

def print_update(battle=False):

	if battle:
		attacker, defender, winner, loser = battle
		print()
		print('BATTLE!', attacker, 'attacks', defender)
		print('Winner', winner, winner.battle_score)
		print('Loser', loser, loser.battle_score)
		last_wp = loser.last_weapon
		if last_wp:
			print(loser, 'drops weapon ->', last_wp)
			if last_wp == winner.weapon:
				print(winner, 'picks up ->', winner.weapon)

	if numpy_: print(board)
	print('{:12}'.format('Positions'), dict(occupied))
	print('{:12}'.format('Free Weapons'), dict(weaponised))

def play():
	''' get down and play '''
	
	m = 0
	for move in get_moves():

		m += 1
		pre_occupied = False

		# get knight and direction
		kn, rxn = move.split(C._SEP)
		k = knights[kn]

		# we only care about knights still on board
		if k.alive:

			# static player does not move
			if k == static_player: continue

			print('\n',f'{m}:',k.alpha,'->',rxn)
			
			# figure out where to move to
			delta = C.deltas[rxn]
			move_to = tuple([(i+j) for i,j in zip(k.position, delta)])

			# flag if already occupied - do this before calling shift
			occupier = knights_here(move_to)
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
			# for knights: remove from old position, add to new
			if Knight.offboard(move_to): 
				last_wp = k.last_weapon
				if last_wp is not None:
					update_board(
						'weapon', last_wp, last_wp.position, 'throw')
			update_board('knight', k, k.last_position, 'old')
			update_board('knight', k, k.position, 'new')
			print_update()		
				
			# no further action except if two knights meet
			# since two's a crowd, they fight
			if pre_occupied:
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
				update_board('knight', loser, loser.position, 'dead')
				update_board('knight', winner, winner.position, 'old')
				update_board('knight', winner, winner.position, 'new')
				print_update((k,occupier,winner,loser))
								
class GameEncoder(json.JSONEncoder):
	''' custom JSON encoder to output each record on single line
		
		default json output 
		{ 
			'a':
				[
					'foo',
					'bar'
				]
		} 
		when we want: 
		{
			'a': ['foo', 'bar']  <- all on single line
		}
	'''

	def iterencode(self, o, _one_shot=False):
		''' a customised implementation
			https://github.com/python/cpython/blob/3.8/Lib/json/encoder.py
		'''

		indent_ = 0

		for ln in super(GameEncoder, self).iterencode(o, _one_shot=_one_shot):

	  		if ln.startswith('['):
	  			indent_ += 1
	  			ln = re.sub(r'\s*', '', ln)

	  		elif 0 < indent_:
	  			ln = re.sub(r'\s*', '', ln)

	  		if ln.endswith(']'):
	  			indent_ -= 1
	  		
  			yield ln

  		
def final_state():
	''' dump json '''

	# create dictionary with knights and weapons
	jdict = {}
	
	for obj in knights.values():
		item = obj.weapon
		item = item.name.lower() if item is not None else 'null' 
		jdict[obj.name.lower()] = \
			[obj.position, obj.status, item, obj.attack, obj.defence] 
	
	for obj in weapons.values():
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
		create_board()	# numpy array

	load_weapons()	# from constants
	load_knights()	# from constants
	
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
	
