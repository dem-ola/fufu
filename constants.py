''' constant variables '''

_FILE 		= 'moves.txt'

_FLAG 		= 'GAME'
_START 		= _FLAG + '-START'
_END 		= _FLAG + '-END'
_SEP 		= ':'
_FLAGS 		= [_START, _END]

board_shape	= 13
static_square = (6, 6)

deltas		= {			
	'N': (-1, 0),
	'S': (1, 0),
	'E': (0, 1),
	'W': (0, -1),
}

_MIN_BASE = 0
_MAX_BASE = 2
_STATIC_SCORE = 5

knights		= 	(
	# name, starting (y,x)
	('Amber', (0, 0)),
	('Blue', (0, 4)),
	('Cream', (0, 8)),
	('Daffodil', (0, 12)),
	('Ebony', (4, 12)),
	('Fog', (6, 6)),
	('Green', (8, 12)),
	('Hazel', (12, 12)),
	('Jam', (12, 8)),
	('Kiwi', (12, 4)), 
	('Lavender', (12, 0)),
	('Mocha', (8, 0)),
	('Navy', (4, 0)),
)

weapons		= (
	# alpha, starting (y,x), rank
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
	
_SURPRISE_SCORE = 0.5

players_ 	= [kn[0][0] for kn in knights]	# -> first letter
directions	= [d for d in deltas]			# -> NEWS





