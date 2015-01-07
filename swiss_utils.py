from swiss_player import Player
from random import shuffle

def get_ranked_player_list(player_list):
	return sorted( player_list, reverse = True, key = lambda p:(p.match_win, p.opp_match_win_percent, p.game_win_percent, p.opp_game_win_percent, p.hidden_rank) )

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

def dropout_players( player_list ):
	temp_player_list = player_list.copy()
	active_filter = list(filter( lambda x: x.is_bye or not x.is_active , temp_player_list))
	for p in active_filter:
		temp_player_list.remove( p )
	print( "Select any players who are dropping out (Enter to continue)" )
	
	while True:
		choice = input()
		if choice == "":
			bye_filter = filter( lambda x: x.is_bye == True, player_list)
			bye = next(bye_filter)
			if( len(temp_player_list) % 2 == 1 ):
				bye.is_active = True
			else:
				bye.is_active = False
			break
		
		remove_filter = list( filter(lambda x: choice == x.name, temp_player_list) )
		for p in remove_filter:
				print( p.name, "has been dropped out.")
				p.is_active = False
				temp_player_list.remove(p)
		
		if not remove_filter:
			print( choice, "is not a valid name.")

# Reduce effect of floating point errors
def is_equal_rank_tiebreakers( p1, p2 ):
	return p1.match_win == p2.match_win \
	and abs(p1.opp_match_win_percent - p2.opp_match_win_percent) < 0.0001 \
	and abs(p1.game_win_percent - p2.game_win_percent) < 0.0001 \
	and abs(p1.opp_game_win_percent - p2.opp_game_win_percent) < 0.0001

def is_equal_rank_no_tiebreakers(p1, p2):
	return p1.match_win == p2.match_win