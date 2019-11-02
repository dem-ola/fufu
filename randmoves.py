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
knights = [k[0] for k in C.knights]
directions = list(C.deltas.keys())
sep = C._SEP

# to avoid early drownings we'll prescribe
# directions that take knights inwards - to safety
# later we'll say what proportion of moves to be 'safe'
safe_directions = {
	'R': ['S', 'E'],
	'B': ['N', 'E'],
	'G': ['N', 'W'],
	'Y': ['S', 'W'],
}

safe = 0.5		# keep this proportion of steps 'safe'
def_moves = 100	# default number of game moves

def choice(lst): return random.choice(lst)

def main(moves=def_moves):
	with open(C._FILE, 'w') as f:
		f.write(C._START+'\n')
		for i in range(moves):

			rand_k = choice(knights)[0]
			rand_d = choice(directions)

			if i < int(moves * safe):
				rand_d = choice(safe_directions[rand_k])

			move = choice(rand_k) + sep + choice(rand_d)
			f.write(move+'\n')

		f.write(C._END)


if __name__ == '__main__':	
	args = sys.argv
	if len(args) > 1:
		try: 	def_moves = int(args[1])
		except:	pass
	main(def_moves)

