from sys import argv
from math import log2, ceil
from swiss_pairing import random_pairings, score_based_pairings
from swiss_utils import create_player_list, update_tiebreakers, dropout_players
from swiss_document import publish_round_pairing, publish_final_standings

def input_pairing_results( pairings ):
	count = 1
	print( "\n\nPairings: ")
	for a, b in pairings:
		print(count, "-", a.name, "vs", b.name)
	print("")

	for a, b in pairings:

		result_input = ""

		if a.is_bye:
			print("{b} receives a bye".format(b=b.name))
			b.update_score(a, 2, 0)
		elif b.is_bye:
			print("{a} receives a bye".format(a=a.name))
			a.update_score(b, 2, 0)
		else:
			result_input = ""
			while result_input not in ["2-0", "2-1", "1-2", "0-2"]:
				print("Enter score for {a} vs {b}".format(a=a.name, b=b.name))
				result_input = input()

		if result_input == "2-0":
			a.update_score(b, 2, 0)
			b.update_score(a, 0, 2)
			print( a.name, "beat", b.name, "2-0")

		if result_input == "2-1":
			a.update_score(b, 2, 1)
			b.update_score(a, 1, 2)
			print( a.name, "beat", b.name, "2-1")

		if result_input == "0-2":
			a.update_score(b, 0, 2)
			b.update_score(a, 2, 0)
			print( b.name, "beat", a.name, "2-0")

		if result_input == "1-2":
			a.update_score(b, 1, 2)
			b.update_score(a, 2, 1)
			print( b.name, "beat", a.name, "2-1")

# Main Tournament Loop
def run_tournament(player_list):
	previous_pairings = set()
	num_rounds = ceil(log2(len(player_list)))
	
	for r in range(num_rounds):
		active_player_list = []
		for p in player_list:
			if p.is_active:
				active_player_list.append(p)

		if r == 0:
			pairings = random_pairings(active_player_list)
		else:
			pairings = score_based_pairings(active_player_list, previous_pairings)

		previous_pairings.update(pairings)
		publish_round_pairing(r, player_list, pairings, num_rounds)
		input_pairing_results(pairings)
		update_tiebreakers(player_list)
		
		if r != num_rounds - 1:
			dropout_players(player_list)

	publish_final_standings(player_list, num_rounds)

# Main function
if __name__ == "__main__":
	script, player_file = argv

	player_list = create_player_list(player_file)

	run_tournament(player_list)