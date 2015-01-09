from sys import argv
from swiss_document import publish_round_pairing, publish_end_of_swiss_standings, publish_finals_document
from swiss_input import input_pairing_results, input_dropout_players, input_finals_match_result
from swiss_pairing import random_pairings, score_based_pairings, seeded_finals_pairings, unseeded_finals_pairings
from swiss_utils import create_player_list, update_tiebreakers, get_num_rounds, get_top_cut_count, get_finals_players

# Tournament Method
def run_tournament(player_list):
	# Swiss Rounds
	previous_pairings = set()
	num_rounds = get_num_rounds(len(player_list))
	
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
	top_cut_player_count = get_top_cut_count(player_list)
	publish_end_of_swiss_standings(player_list, num_rounds, top_cut_player_count)

	# Finals
	remaining_players = get_finals_players(player_list, top_cut_player_count)
	players_in_rank_order = []
	completed_finals_rounds = []
	while len(remaining_players) != 1:
		# Create next batch of matches, and add previous matches to completed if required
		if len(remaining_players) == top_cut_player_count:
			current_finals_round = seeded_finals_pairings(remaining_players, top_cut_player_count)
		else:
			# Start new round by making the next set of matches
			completed_finals_rounds = current_finals_round + completed_finals_rounds
			current_finals_round = unseeded_finals_pairings(remaining_players)

		remaining_players = []	
		for match in current_finals_round:
			while match.score1 < 3 and match.score2 < 3:
				publish_finals_document(current_finals_round + completed_finals_rounds)
				input_finals_match_result(match)
			
			# Winner of each match gets put into remaining players
			if match.score1 == 3:
				winner = match.name1
				loser = match.name2
			else:
				winner = match.name2
				loser = match.name1

			remaining_players.append(winner)
			players_in_rank_order.append(loser)

	# Add final match, and final player to defeated (for ranking purposes)
	completed_finals_rounds = current_finals_round + completed_finals_rounds
	players_in_rank_order.append(remaining_players.pop())
	publish_finals_document(completed_finals_rounds, players_in_rank_order)

# Main function
if __name__ == "__main__":
	script, player_file = argv

	player_list = create_player_list(player_file)

	run_tournament(player_list)