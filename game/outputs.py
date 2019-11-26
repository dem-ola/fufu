'Various outputs - json, stdout'

import json
from fuencoder import GameEncoder
from constants import json_path

def print_update(board=None, fu_dict=None, weap_dict=None, 
                    occupied=None, weaponised=None, a_bat=None, d_bat=None, battle=False):

	if battle:
		attacker, defender, winner, loser = battle
		print()
		print('BATTLE!', attacker, a_bat, 'attacks', defender, d_bat)
		print('Winner', winner, winner.battle_score)
		print('Loser', loser, loser.battle_score)
		last_wp = loser.last_weapon
		if last_wp:
			print(loser, 'drops weapon ->', last_wp)
			if last_wp == winner.weapon:
				print(winner, 'picks up ->', winner.weapon)

	if board is not None: print(board)
	Fs = []
	for f in fu_dict:
		f_ = fu_dict[f]
		Fs.append((f_, f_.attack, f_.defence, f_.weapon.score if f_.weapon else 'None'))
	print('{:12}'.format('Scores'), Fs)
	print('{:12}'.format('Positions'), dict(occupied))
	print('{:12}'.format('Free Weapons'), dict(weaponised))


def final_state(fu_dict=None, weap_dict=None):
	''' dump json '''

	# create dictionary with fus and weapons
	jdict = {}
	
	for obj in fu_dict.values():
		item = obj.weapon
		item = item.name.lower() if item is not None else 'null' 
		jdict[obj.name.lower()] = \
			[obj.position, obj.status, item, obj.attack, obj.defence] 
	
	for obj in weap_dict.values():
		obj_owner = obj.owner
		jdict[obj.name.lower()] = \
			[obj.position, 
			obj_owner.name.lower() if obj_owner is not None else False]

	# create a json string to display - note: custom encoder
	json_ = json.dumps(jdict, indent=2, cls=GameEncoder)
	print()
	print(json_)

	# write to file - note: custom encoder
	with open(json_path, 'w') as jf:
		json.dump(jdict, jf, indent=2, cls=GameEncoder)