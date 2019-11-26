from fus import fus

FLAG 		= 'GAME'
START 		= FLAG + '-START'
END 		= FLAG + '-END'
SEP 		= ':'

def valid_file(f):
	''' checks if moves input file is valid '''

	# check game start
	top = f.read(len(START))
	top_ = top.startswith(START)

	# check game end
	f.seek(0,2)              		# go to end of file
	f.seek(f.tell() - len(END))  # go backwards
	end = f.read()
	end_ = end.endswith(END)

	# check mid sections for proper syntax
	# we can choose not to do this and just skip invalid lines
	# but with large game input files this could be harder to debug
	# so we'll check all the lines upfront
	# blank lines will be skipped
	mid_ = True
	f.seek(0)		# move back to top of file
	for line in f:
		lenn = len(line.strip())
		if not line.startswith(FLAG) and lenn > 0:
			if lenn != 3 or \
				line[0] not in [name[0][0] for name in fus] or \
				line[1] != SEP or \
				line[2] not in ['N','E','W','S']:
				mid_ = False
				break

	return all((top_, end_, mid_))