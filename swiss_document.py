from pylatex import Document, Section, Subsection, Table, Package
from pylatex.utils import bold, escape_latex
from swiss_utils import is_equal_rank_tiebreakers, is_equal_rank_no_tiebreakers, get_ranked_player_list

def add_pairings(doc, pairings):
	with doc.create(Subsection('Pairings', False)):
			with doc.create(Table('llcr')) as table:
				count = 1
				for a, b in pairings:
					if a.is_bye:
						table.add_row((bold(str(count)), b.name, "", bold("BYE")))
					elif b.is_bye:
						table.add_row((bold(str(count)), a.name, "", bold("BYE")))
					else:
						table.add_row((bold(str(count)), a.name, "vs", b.name))
					count += 1

def add_standings_full(doc, player_list, cutoff = False, cutoff_num = 0):
	sp = get_ranked_player_list(player_list)
	rank = 1
	previous_player = None
	dropped_section = False

	with doc.create(Subsection('Standings', False)):
		with doc.create(Table('|c|l|cc|rrr|')) as table:
			table.add_hline()
			table.add_row(("Rank", "Player", "Wins", "Losses", "TB1", "TB2", "TB3"))
			table.add_hline()
			
			for i, player in enumerate(sp):
				if player.is_bye:
					continue
				if previous_player != None and not is_equal_rank_tiebreakers(previous_player, player):
					rank = i + 1
				
				tb1 = '{0:.1%}'.format(player.opp_match_win_percent)
				tb2 = '{0:.1%}'.format(player.game_win_percent)
				tb3 = '{0:.1%}'.format(player.opp_game_win_percent)

				if not player.is_active:
					if not dropped_section:
						table.add_hline()
						dropped_section = True
					table.add_row(("X", player.name, player.match_win, player.match_loss, escape_latex(tb1), escape_latex(tb2), escape_latex(tb3)))
				else:
					table.add_row((rank, player.name, player.match_win, player.match_loss, escape_latex(tb1), escape_latex(tb2), escape_latex(tb3)))
					previous_player = player

				if cutoff and i == cutoff_num - 1:
					table.add_hline()

			table.add_hline()

def add_standings_simple(doc, player_list):
	sp = get_ranked_player_list(player_list)
	rank = 1
	previous_player = None
	dropped_section = False

	with doc.create(Subsection('Standings', False)):
		with doc.create(Table('|c|l|cc|')) as table:
			table.add_hline()
			table.add_row(("Rank", "Player", "Wins", "Losses"))
			table.add_hline()
			
			for i, player in enumerate(sp):
				if player.is_bye:
					continue
				if previous_player != None and not is_equal_rank_no_tiebreakers(previous_player, player):
					rank = i + 1

				if not player.is_active:
					if not dropped_section:
						table.add_hline()
						dropped_section = True
					table.add_row(("X", player.name, player.match_win, player.match_loss))
				else:
					table.add_row((rank, player.name, player.match_win, player.match_loss))
					previous_player = player

			table.add_hline()

def add_previous_results(doc, player_list, num_rounds):
	sp = sorted( player_list, key = lambda p:p.name )

	with doc.create(Subsection('Previous Round Results', False)):
				with doc.create(Table('|l|' + 'c|' * num_rounds)) as table:
					# Creates the top row containing the right number of rounds in the tournament
					title_list = ["Player"]
					for i in range(num_rounds):
						title_list.append("Round " + str(i+1))
					
					table.add_hline()
					table.add_row(title_list)
					table.add_hline()

					for p in sp:
						if p.is_bye:
							continue

						player_row = [p.name]
						result_row = [""]

						for i in range(len(p.opponents)):
							player_row.append(bold(p.opponents[i].name))
							result_row.append(p.results[i])
						
						for j in range(num_rounds - len(p.opponents)):
							player_row.append("")
							result_row.append("")
						
						table.add_row(player_row)
						table.add_row(result_row)
						table.add_hline()

def add_elimination_matches(doc, matches):
	for match in matches:
		with doc.create(Subsection('', False)):
			with doc.create(Table('| c c c |')) as table:
				table.add_hline()
				table.add_row(("", bold(match.description), ""))
				table.add_hline()
				table.add_row((match.name1, "vs", match.name2))
				table.add_row((bold(str(match.score1)), "", bold(str(match.score2))))
				table.add_hline()
				table.add_row(("", bold("Game Results"), ""))
				table.add_hline()
				for i in range(len(match.game_winners)):
					table.add_row(("Game " + str(i+1), "", match.game_winners[i]))
				table.add_hline()

def add_final_ranks(doc, player_list):
	# The list is from first eliminated to last eliminated
	rank_list = player_list
	rank_list.reverse()
	rank = 1
	top_cut = 1

	with doc.create(Table('p {4cm} | c | c | p {4cm}')) as table:
		table.add_hline(2,3)
		for player in rank_list:
			if rank == 1:
				table.add_row(("", "Winner", player, ""))
			elif rank == 2:
				table.add_row(("", "Runner Up", player, ""))
			else:
				while rank > top_cut:
					top_cut *= 2
				table.add_row(("", "Top " + str(top_cut), player, ""))

			table.add_hline(2,3)
			rank += 1


def publish_round_pairing(r_num, player_list, pairings, num_rounds):
	doc = Document("Round" + str(r_num + 1))
	doc.packages.append(Package('geometry', options=['lmargin=3cm']))

	with doc.create(Section("Round " + str(r_num + 1) + " of " + str(num_rounds), False)):
		add_pairings(doc, pairings)

	if r_num >= 2:
		add_standings_full(doc, player_list)
	else:
		add_standings_simple(doc, player_list)
	add_previous_results(doc, player_list, num_rounds)

	doc.generate_pdf()

def publish_end_of_swiss_standings(player_list, num_rounds, cutoff_players):
	doc = Document("EndOfSwiss")
	doc.packages.append(Package('geometry', options=['lmargin=3cm']))

	with doc.create(Section("End of Swiss Results", False)):
		add_standings_full(doc, player_list, True, cutoff_players)
		add_previous_results(doc, player_list, num_rounds)

	doc.generate_pdf()

def publish_finals_document(finals_matches, players_in_rank_order = []):
	doc = Document("Finals")
	doc.packages.append(Package('geometry', options=['lmargin=5cm']))

	if players_in_rank_order:
		with doc.create(Section("Finals Rankings", False)):
			add_final_ranks(doc, players_in_rank_order)

	with doc.create(Section("Finals Playoff Matches", False)):
		add_elimination_matches(doc, finals_matches)

	doc.generate_pdf()