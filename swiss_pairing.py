from random import shuffle
from swiss_utils import get_ranked_player_list

# Used for first round pairing only
# Shuffle list, then return a set containing every (n*2)th player vsing (n*2+1)th player
def random_pairings(player_list):
	player_list_copy = player_list[:]
	shuffle(player_list_copy)
	return list(frozenset(x) for x in zip(player_list_copy[::2], player_list_copy[1::2]) )

# Recursion pairing for post-first round
# If the last pair fails, keep switching the remaining players until correct
def score_based_pairings(player_list, previous):
	sp = get_ranked_player_list(player_list)

	def pair_players(players):
		if len(players) == 2:
			if frozenset(players) in previous:
				return None
			else:
				return [frozenset(players)]

		for i in range(len(players) - 1):
			for j in range(i+1, len(players)):
				pair = frozenset([players[i], players[j]])

				if pair not in previous:
					sub_list = players[:i] + players[i+1:j] + players[j+1:]
					rec = pair_players(sub_list)

					# Recursion failure check
					if rec:
						rec.append( pair )
						return rec
	
	return pair_players(sp)