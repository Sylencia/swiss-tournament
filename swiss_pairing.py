from random import shuffle
from swiss_utils import get_ranked_player_list
from swiss_classes import FinalsMatch

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

# Finals random_pairings
def seeded_finals_pairings(players, num_players):
	
	# returns a new seed list for the new number of teams
	def seed(num_teams, seed_list):
		new_seed_list = []
		for seed in seed_list:
			new_seed_list += [ seed, num_teams + 1 - seed ]
		return new_seed_list

	teams = 1
	seed_list = [1]
	while teams != num_players:
		teams *= 2
		seed_list = seed(teams, seed_list)

	# We have seed order now, so make matches in order
	if num_players == 2:
		description = "Grand Finals"
	else:
		description = "Top " + str(num_players)

	pairings = []
	for x, y in zip(seed_list[::2], seed_list[1::2]):
		# Subtract 1 for indexing
		pairings.append( FinalsMatch(players[x-1], players[y-1], description) )
	return pairings

def unseeded_finals_pairings(player_list):
	if len(player_list) == 2:
		description = "Grand Finals"
	else:
		description = "Top " + str(num_players)

	pairings = []
	for x, y in zip(player_list[::2], player_list[1::2]):
		pairings.append( FinalsMatch(x, y, description) )
	return pairings