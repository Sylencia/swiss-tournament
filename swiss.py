from sys import argv
from math import log2, ceil
from swiss_pairing import random_pairings, score_based_pairings
from swiss_utils import create_player_list, update_tiebreakers, dropout_players
from swiss_document import publish_round_pairing, publish_final_standings
from swiss_input import input_pairing_results

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