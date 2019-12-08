''' Fighting algorithm '''

WIN_BONUS = 0.5

def fight(challenger, defender):
	''' determine fight winner based on higer score '''

	c_score = challenger.attack + \
				challenger.defence * 0.5 + \
					(challenger.weapon.score if challenger.weapon else 0)

	d_score = 0
	if defender.static:
		d_score = defender.defence + defender.weapon.score
	else:
		d_score = defender.defence + \
					defender.attack * 0.5 + \
					(defender.weapon.score if defender.weapon else 0)

	challenger.battle_score = c_score
	defender.battle_score = d_score

	#  declare winner/loser
	# winners get a bonus
	# they also get weapons rescored
	# as weapons could be damaged/enhanced during fight

	if c_score > d_score:
		winner = challenger
		challenger.attack += WIN_BONUS
		if challenger.weapon is not None: challenger.weapon.rescore()
		loser = defender
	else: # including draws - here defender considered winner
		loser = challenger
		winner = defender
		defender.defence += WIN_BONUS
		if defender.weapon is not None: defender.weapon.rescore()

	return winner, loser