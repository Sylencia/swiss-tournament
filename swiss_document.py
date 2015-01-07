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

def add_standings_full(doc, player_list, cutoff=False):
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

				if cutoff and i == 3:
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

					for p in player_list:
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

def add_elimination_bracket(doc, finals_matches, winner):
	with doc.create(Subsection('Bracket', False)):
				with doc.create(Table('| c | c | c |')) as table:
					table.add_hline()
					table.add_row(("Semi Finals", "Grand Finals", "Tournament Winner"))
					table.add_hline()
					table.add_empty_row()
					table.add_hline(1,1)
					table.add_row((bold(finals_matches[0].name1), "", ""))
					table.add_empty_row()
					table.add_hline(2,2)
					table.add_row((finals_matches[0].score, bold(finals_matches[2].name1), ""))
					table.add_empty_row()
					# table.add_hline(2,2)
					table.add_row((bold(finals_matches[0].name2), "", ""))
					table.add_hline(1,1)
					# table.add_hline(3,3)
					table.add_empty_row()
					table.add_row(("", finals_matches[2].score, bold(winner)))
					table.add_empty_row()
					# table.add_hline(3,3)
					table.add_hline(1,1)
					table.add_row((bold(finals_matches[1].name1), "", ""))
					# table.add_hline(1,2)
					table.add_empty_row()
					table.add_row((finals_matches[1].score, bold(finals_matches[2].name2), ""))
					table.add_hline(2,2)
					table.add_empty_row()
					table.add_row((bold(finals_matches[1].name2), "", ""))
					table.add_hline(1,1)
					table.add_empty_row()
					table.add_hline()

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

def publish_end_of_swiss_standings(player_list, num_rounds):
	doc = Document("EndOfSwiss")
	doc.packages.append(Package('geometry', options=['lmargin=3cm']))

	with doc.create(Section("End of Swiss Results", False)):
		add_standings_full(doc, player_list, True)
		add_previous_results(doc, player_list, num_rounds)

	doc.generate_pdf()

def publish_finals_document(finals_matches, winner = ""):
	doc = Document("Finals")
	doc.packages.append(Package('geometry', options=['lmargin=5cm']))

	with doc.create(Section("Top 4", False)):
		add_elimination_bracket(doc, finals_matches, winner)

	doc.generate_pdf()