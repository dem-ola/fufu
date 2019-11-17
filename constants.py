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

_FU_ATTACK_SKILL = (0, 3) 
_FU_DEFENCE_SKILL = (0, 5)
_WP_SCORE = (1, 2)
_STATIC_SKILL = 5
_WIN_BONUS = 0.5

knights		= 	(
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

players_ 	= [kn[0][0] for kn in knights]	# -> first letter
directions	= [d for d in deltas]			# -> NEWS





