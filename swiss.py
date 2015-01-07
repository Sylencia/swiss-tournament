from sys import argv
from math import log2, ceil
from swiss_pairing import random_pairings, score_based_pairings, create_finals_pairings
from swiss_utils import create_player_list, update_tiebreakers, update_finals_bracket
from swiss_document import publish_round_pairing, publish_end_of_swiss_standings, publish_finals_document
from swiss_input import input_pairing_results, input_dropout_players, input_finals_match_result

# Tournament Method
def run_tournament(player_list):
	# Swiss Rounds
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
			input_dropout_players(player_list)

	# End of Swiss Rounds
	publish_end_of_swiss_standings(player_list, num_rounds)

	# Finals
	finals = create_finals_pairings(player_list)
	winner = ""

	for i in range(len(finals)):
		publish_finals_document(finals)
		match_winner = input_finals_match_result(finals[i])
		winner = update_finals_bracket(i, match_winner, finals)

	publish_finals_document(finals, winner)

# Main function
if __name__ == "__main__":
	script, player_file = argv

	player_list = create_player_list(player_file)

	run_tournament(player_list)