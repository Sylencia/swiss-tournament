from swiss_classes import Player
from random import shuffle

def get_ranked_player_list(player_list):
	return sorted( player_list, reverse = True, key = lambda p:(p.is_active, p.match_win, p.opp_match_win_percent, p.game_win_percent, p.opp_game_win_percent, p.hidden_rank) )

# Creates a list of Players from given names
def create_player_list(filename):
	players=[]

	with open(filename) as f:
		content = f.readlines()
		hidden_ranks = list(range(len(content)))
		shuffle(hidden_ranks)
		for line in content:
			players.append(Player(line.strip(), False, True, hidden_ranks.pop()))

	# Add an extra bye player that is active dependent on whether or not it is originally needed
	players.append(Player( "BYE", True, len(players) % 2 == 1, 0))

	return players

def update_tiebreakers( player_list ):
	for player in player_list:
		player.update_tiebreakers()

def update_finals_bracket(match_num, match_winner, finals):
	if match_num == 0:
		finals[2].update_name(match_winner, 1)
	elif match_num == 1:
		finals[2].update_name(match_winner, 2)
	else:
		return match_winner
	return ""

# Reduce effect of floating point errors
def is_equal_rank_tiebreakers( p1, p2 ):
	return p1.match_win == p2.match_win \
	and abs(p1.opp_match_win_percent - p2.opp_match_win_percent) < 0.0001 \
	and abs(p1.game_win_percent - p2.game_win_percent) < 0.0001 \
	and abs(p1.opp_game_win_percent - p2.opp_game_win_percent) < 0.0001

def is_equal_rank_no_tiebreakers(p1, p2):
	return p1.match_win == p2.match_win