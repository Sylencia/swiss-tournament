from swiss_classes import Player
from random import shuffle
from math import log2, ceil

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

# Reduce effect of floating point errors
def is_equal_rank_tiebreakers( p1, p2 ):
	return p1.match_win == p2.match_win \
	and abs(p1.opp_match_win_percent - p2.opp_match_win_percent) < 0.0001 \
	and abs(p1.game_win_percent - p2.game_win_percent) < 0.0001 \
	and abs(p1.opp_game_win_percent - p2.opp_game_win_percent) < 0.0001

def is_equal_rank_no_tiebreakers(p1, p2):
	return p1.match_win == p2.match_win

def get_num_rounds(player_count):
	if player_count > 2050:
		return 12
	else:
		return ceil(log2(player_count))

def get_top_cut_count(player_list):
	active_players = sum( p.is_active and not p.is_bye for p in player_list)
	if active_players > 1024:
		return 32
	elif active_players > 256:
		return 16
	elif active_players > 32:
		return 8
	elif active_players > 8:
		return 4
	else:
		return 2

def get_finals_players(player_list, cutoff):
	sp = get_ranked_player_list(player_list)
	return list( player.name for player in sp[:cutoff] )