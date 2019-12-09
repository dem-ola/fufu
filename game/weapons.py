''' Describes weapons '''

import random

# skill scores
MIN_SKILL = 1
MAX_SKILL = 2

weapons		= (
	# name, starting coordinates (y,x) <- NOT x,y
	('Qire', (6,6)),
	('Rxe', (2,2)),
	('Sai', (2,6)),
	('Tusket', (2,10)),
	('Umbrella', (6,10)),
	('Vistol', (10,10)),
	('Wand', (10,6)),
	('Yelmet', (10,2)),
	('Zagger', (6,2)),
)

class Weapon():
	''' Weapons '''

	def __init__(self, name, startpos):
		self.alpha = name[0]
		self.name = name
		self.startpos = startpos	# y,x tuple
		self.curpos = startpos
		self.owner = None
		self.static = int(startpos[0]) == 0
		self.set_score()

	def rescore(self):
		''' after each battle we do this for the winner
			because the weapon could be damaged or enhanced eg sharpened
			during battle '''
		self.set_score()

	def set_score(self):
		self.score = random.randrange(MIN_SKILL, MAX_SKILL + 1)

	def __repr__(self):
		return self.alpha