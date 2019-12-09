import random
from operator import attrgetter
from board import board_shape

# skill scores
ATTACK_SKILL = (0, 3) 
DEFENCE_SKILL = (0, 5)
STATIC_SKILL = 5
STATIC_SQUARE = (6, 6)

fus	= 	(
	# name, starting (y,x)
	('Amber', (0, 0), (255,0,0)),
	('Blue', (0, 4), (255,125,0)),
	('Cream', (0, 8), (255,255,0)),
	('Daffodil', (0, 12), (255,125,125)),
	('Ebony', (4, 12), (0,0,255)),
	('Fog', (6, 6), (0,0,0)),
	('Green', (8, 12), (0,255,255)),
	('Hazel', (12, 12), (160,160,255)),
	('Jam', (12, 8), (250,250,200)),
	('Kiwi', (12, 4), (0,255,0)),
	('Lavender', (12, 0), (200,240, 200)),
	('Mocha', (8, 0), (125,80,80)),
	('Navy', (4, 0), (255,0,255)),
)

class Fu():
	''' fus i.e. players '''

	_static = STATIC_SKILL
	_static_sq = STATIC_SQUARE

	def __init__(self, name, startpos):
		self.alpha = name[0]
		self.name = name
		self.startpos = startpos
		self.curpos = startpos
		self.alive = True
		self.status = 'LIVE'
		self.weapon = None
		self.static = int(startpos[0]) == 0
		self.battle_score = 0 	# for printing winner/loser
		self.set_score()
		
	@staticmethod
	def offboard(move_to):
		''' check if new coordinates still on board '''
		if move_to == 'null':
			return True
		shape = board_shape - 1
		return any(i for i in move_to if i < 0 or i > shape)
		
	def set_score(self):
		if self.startpos == self._static_sq:
			attack = 0
			defence = self._static
		else:
			attack = random.randrange(
				ATTACK_SKILL[0], ATTACK_SKILL[1] + 1)
			defence = random.randrange(
				DEFENCE_SKILL[0], DEFENCE_SKILL[1] + 1)
		self.attack = attack
		self.defence = defence

	def pick_weapon(self, the_weapons):
		''' Fu picks a weapon from square '''
		# only called when Fu doesn't already have a weapon
		# and there are weapons freely available on the square
		# sort weapons by preference/rank and pick highest ranking
		if len(the_weapons) > 1:
			the_weapons.sort(reverse=True, key=attrgetter('rank'))
		picked = the_weapons[0]
		self.weapon = picked

		# update weapon attributes
		picked.owner = self
		picked.curpos = self.curpos

		return picked

	def kaput(self, status):
		''' stuff to do if drowning or dying '''
		if self.weapon is not None: # as None cannot have .owner
			self.weapon.owner = None
		self.weapon = None
		self.alive = False
		self.status = status
		self.attack = 0
		self.defence = 0

	def shift(self, move_to=None, avail_weapons=None):
		''' move Fu '''
		self.curpos = move_to
		if self.weapon is not None:
			self.weapon.curpos = move_to
		return self.weapon

	def __repr__(self):
		return self.alpha