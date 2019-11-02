''' constant variables '''

_FILE 		= 'moves.txt'

_FLAG 		= 'GAME'
_START 		= _FLAG + '-START'
_END 		= _FLAG + '-END'
_SEP 		= ':'
_FLAGS 		= [_START, _END]

deltas		= {			
	'N': (-1, 0),
	'S': (1, 0),
	'E': (0, 1),
	'W': (0, -1),
}

knights		= 	(
	# name, starting (y,x)
	('Red', (0, 0)),
	('Blue', (7, 0)),
	('Green', (7, 7)),
	('Yellow', (0, 7)),
)

weapons		= (
	# alpha, starting (y,x), attack, defence, rank
	('Magic_Staff', (5,2), 1, 1, 3),	# MagicStaff
	('Helmet', (5,5), 0, 1, 1),			# Helmet
	('Dagger', (2,5), 1, 0, 2),			# Dagger
	('Axe', (2,2), 2, 0, 4),			# Axe
)
	
_SURPRISE_SCORE = 0.5

players_ 	= [kn[0][0] for kn in knights]	# -> first letter
directions	= [d for d in deltas]			# -> NEWS





