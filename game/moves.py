''' Calculate next move for next Fu 

    #TODO: make more sophisticated - combine with randmoves?
'''

from constants import move_path
from valid import START, END, valid_file

deltas		= { # not used here yet (in game.py but hopefully later)
	'N': (-1, 0),
	'S': (1, 0),
	'E': (0, 1),
	'W': (0, -1),
}

def get_moves():
	''' get next move from file '''
	with open(move_path) as f:
		if not valid_file(f): # kill + warn if invalid file
			raise Exception('Please use a valid game file')
		else:
			f.seek(0)
			while True:
				line = f.readline().strip()
				if line == END:	# at end of file
					break
				if line not in [START, '']: # skip first line, blanks
					yield line