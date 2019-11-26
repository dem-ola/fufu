''' generate random moves and save to file;
	file saved to is the default in constants.py
	to not overwrite the default:
		amend with open(file ..) below
		or change the constants.py default
'''

from constants import move_path
import random, sys, re
from fus import STATIC_SQUARE, fus as fus_
from valid import START, END, SEP

# get variables
fus = [f for f in fus_]

# to avoid early drownings we'll prescribe
# directions that take players inwards - to safety
safe = 0.7		# proportion of steps 'safe'
def_moves = 200	# default number of game moves

# we need to track each player's position as they move
class Player():
	def __init__(self, name, y, x):
		self.name = name
		self.x = x
		self.y = y

def get_players(fus):
	players = []
	for f in fus:
		players.append(Player(f[0], f[1][0], f[1][1]))
	return players

def choice(lst): 
	return random.choice(lst)

def main(moves=def_moves, safe=safe):
	''' derive moves '''

	players = get_players(fus)
	
	static_y, static_x = STATIC_SQUARE
	safe_moves = int(moves * safe)
	
	
	with open(move_path, 'w') as f:
		f.write(START+'\n')

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

			move = alpha + SEP + go
			f.write(move+'\n')
		f.write(END)


if __name__ == '__main__':	
	args = sys.argv
	if len(args) > 1:
		try: 	def_moves = int(args[1])
		except:	pass
	main(def_moves, safe)

