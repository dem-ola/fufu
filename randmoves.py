#!/usr/bin/python3

''' generate random moves and save to file;
	file saved to is the default in constants.py
	to not overwrite the default:
		amend with open(file ..) below
		or change the constants.py default
'''

import constants as C
import random, sys, re

# get variables
players = [k for k in C.knights]
directions = list(C.deltas.keys())
sep = C._SEP

# to avoid early drownings we'll prescribe
# directions that take knights inwards - to safety
# later we'll say what proportion of moves to be 'safe'
safe_directions = {

	'SE': ['S', 'E'],
	'NE': ['N', 'E'],
	'NW': ['N', 'W'],
	'SW': ['S', 'W'],
}

safe = 0.5		# keep this proportion of steps 'safe'
def_moves = 200	# default number of game moves

def choice(lst): return random.choice(lst)

def main(moves=def_moves):
	with open(C._FILE, 'w') as f:
		f.write(C._START+'\n')
		for i in range(moves):

			player = choice(players)
			pos = player[1]
			rand_p = player[0][0]
			rand_d = choice(directions)

			if i < int(moves * safe):
				d = None
				if pos[0] < 3:
					d = 'SE' if pos[1] < 7 else 'SW'
				elif pos[0] > 10:
					d = 'NE' if pos[1] < 7 else 'NW'
				elif pos[1] < 2:
					rand_d = 'E'
				elif pos[1] > 10:
					rand_d = 'W'
				if d is not None:
					rand_d = choice(safe_directions[d])

			move = choice(rand_p) + sep + choice(rand_d)
			f.write(move+'\n')

		f.write(C._END)


if __name__ == '__main__':	
	args = sys.argv
	if len(args) > 1:
		try: 	def_moves = int(args[1])
		except:	pass
	main(def_moves)

