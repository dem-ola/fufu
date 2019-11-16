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
knights = [k for k in C.knights]
sep = C._SEP

# to avoid early drownings we'll prescribe
# directions that take players inwards - to safety
safe = 0.5		# proportion of steps 'safe'
def_moves = 300	# default number of game moves

# we need to track each player's position as they move
class Player():
	def __init__(self, name, y, x):
		self.name = name
		self.x = x
		self.y = y

def get_players(knights):
	players = []
	for k in knights:
		players.append(Player(k[0], k[1][0], k[1][1]))
	return players

players = get_players(knights)

def choice(lst): return random.choice(lst)

def main(moves=def_moves, safe=safe):
	static_y, static_x = C.static_square
	safe_moves = int(moves * safe)
	with open(C._FILE, 'w') as f:
		f.write(C._START+'\n')

		for i in range(moves):

			# choose player and get position
			chosen = choice(players)
			alpha, y, x = chosen.name[0], chosen.y, chosen.x

			# choose an axis to move along based on position relative to static
			diff_y, diff_x = y - static_y, x - static_x
			chosen_axis = choice((0, 1)) # choose a random axis
			
			# get direction and update player position
			go = ''
			if chosen_axis == 0:
				if i < safe_moves:
					
					go = 'S' if diff_y <= 0 else 'N'
				else:
					go = choice(('S', 'N'))
				chosen.y = y + 1 if go == 'S' else y - 1
			else:
				if i < safe_moves:
					
					go = 'E' if diff_x <= 0 else 'W'
				else:
					 go = choice(('E', 'W'))
				chosen.x = x + 1 if go == 'E' else x - 1

			move = alpha + sep + go
			f.write(move+'\n')
		f.write(C._END)


if __name__ == '__main__':	
	args = sys.argv
	if len(args) > 1:
		try: 	def_moves = int(args[1])
		except:	pass
	main(def_moves, safe)

