import random
import constants as C 	# constants' namespace

# skill scores
ATTACK_SKILL = (0, 3) 
DEFENCE_SKILL = (0, 5)
STATIC_SKILL = 5

fus	= 	(
	# name, starting (y,x)
	('Amber', (0, 0), (255,191,0)),
	('Blue', (0, 4), (0,0,255)),
	('Cream', (0, 8), (100,99,82)),
	('Daffodil', (0, 12), (100,100,19)),
	('Ebony', (4, 12), (10,10,10)),
	('Fog', (6, 6), (150,150,150)),
	('Green', (8, 12), (0,255,0)),
	('Hazel', (12, 12), (119,101,54)),
	('Jam', (12, 8), (255,0,0)),
	('Kiwi', (12, 4), (134,241,81)),
	('Lavender', (12, 0), (230,230,250)),
	('Mocha', (8, 0), (111,55,45)),
	('Navy', (4, 0), (0,0,50)),
)

class Fu():
	''' fus i.e. players '''

	_static = STATIC_SKILL
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
		if self.position == self._static_sq:
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
                    #FIXME: reaching outside class not allowed
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