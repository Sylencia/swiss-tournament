class Player:
	def __init__(self, name, bye, active, hidden_rank):
		self.name = name
		self.is_bye = bye
		self.is_active = active
		self.hidden_rank = hidden_rank
		# Win / Loss (matches)
		self.match_win = 0
		self.match_loss = 0
		self.match_win_percent = 0
		# Win / Loss (games)
		self.game_win = 0
		self.game_loss = 0
		self.game_win_percent = 0 # Tiebreaker 2
		# Opponents
		self.opponents = []
		self.results = []
		self.opp_match_win_percent = 0 # Tiebreaker 1
		self.opp_game_win_percent = 0 # Tiebreaker 3

	def update_score(self, opponent, games_won, games_lost):
		# Add games won and lost
		self.game_win += games_won
		self.game_loss += games_lost

		# Determine if the player won or lost
		if games_won == 2:
			self.match_win += 1
		else: # lost
			self.match_loss += 1

		self.match_win_percent = max(1/3, self.match_win / (self.match_win + self.match_loss))
		self.game_win_percent = max(1/3, self.game_win / (self.game_win + self.game_loss))
		self.opponents.append( opponent )
		self.results.append( str(games_won) + "-" + str(games_lost))

	def update_tiebreakers( self ):
		self.opp_match_win_percent = 0
		self.opp_game_win_percent = 0
		
		total_match_win_percent = 0
		total_game_win_percent = 0
		num_opponents = 0
		
		for opp in self.opponents:
			if opp.is_bye:
				continue
			
			total_match_win_percent += opp.match_win_percent
			total_game_win_percent += opp.game_win_percent
			num_opponents += 1

		self.opp_match_win_percent = total_match_win_percent / max(1, num_opponents)
		self.opp_game_win_percent = total_game_win_percent / max(1, num_opponents)