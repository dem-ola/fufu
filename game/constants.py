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

_WIN_BONUS = 0.5

directions	= [d for d in deltas]			# -> NEWS





