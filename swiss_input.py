from random import choice, randint

def input_pairing_results( pairings ):
	while not len(pairings) == 0:
		print( "\nPairings: ")
		count = 0

		for a, b in pairings[:]:
			if a.is_bye:
				print("{b} receives a bye".format(b=b.name))
				b.update_score(a, 2, 0)
				del(pairings[count])
			elif b.is_bye:
				print("{a} receives a bye".format(a=a.name))
				a.update_score(b, 2, 0)
				del(pairings[count])
			else:
				print(count+1, "-", a.name, "vs", b.name)
				count += 1
		
		print("\nSelect a match to enter a result for.")
		selection = input()
		try:
			val = int(selection)
			if val <= 0 or val > len(pairings):
				print("Please enter a number between 1 and", len(pairings))
				continue

			# Get result
			a, b = pairings[val-1]
			result_input = "-"
			while result_input not in ["2-0", "2-1", "1-2", "0-2", ""]:
				print("Enter score for {a} vs {b}".format(a=a.name, b=b.name))
				result_input = input()
			
			if(result_input == ""):
				print("Match input cancelled.")
				continue

			if result_input == "2-0":
				a.update_score(b, 2, 0)
				b.update_score(a, 0, 2)
			if result_input == "2-1":
				a.update_score(b, 2, 1)
				b.update_score(a, 1, 2)
			if result_input == "0-2":
				a.update_score(b, 0, 2)
				b.update_score(a, 2, 0)
			if result_input == "1-2":
				a.update_score(b, 1, 2)
				b.update_score(a, 2, 1)
			
			print( b.name, "beat", a.name, result_input)
			del(pairings[val-1])

		except ValueError:
			print("Please enter a number between 1 and", len(pairings))

def input_dropout_players( player_list ):
	temp_player_list = player_list.copy()
	active_filter = list(filter( lambda x: x.is_bye or not x.is_active , temp_player_list))
	for p in active_filter:
		temp_player_list.remove( p )
	
	while True:
		print( "\nEnter the name of a player who is dropping out (Enter to continue tournament)" )
		choice = input()
		if choice == "":
			bye_filter = filter( lambda x: x.is_bye == True, player_list)
			bye = next(bye_filter)
			if( len(temp_player_list) % 2 == 1 ):
				bye.is_active = True
			else:
				bye.is_active = False
			break
		
		remove_filter = list( filter(lambda x: choice.lower() == x.name.lower(), temp_player_list) )
		for p in remove_filter:
				print( p.name, "has dropped out.")
				p.is_active = False
				temp_player_list.remove(p)
		
		if not remove_filter:
			print( choice, "is not a valid name.")

def input_finals_match_result( match ):
	p1_score = 0
	p2_score = 0

	while p1_score < 3 and p2_score < 3:
		print("\n")
		print(match.name1, "vs", match.name2, ":", p1_score, "-", p2_score)
		print("Enter result: ")
		result = input()
		while result.lower() not in [match.name1.lower(), match.name2.lower()]:
			result = input()

		if result.lower() == match.name1.lower():
			p1_score += 1

		if result.lower() == match.name2.lower():
			p2_score += 1

	match.update_score(p1_score, p2_score)
	
	if p1_score >= 3:
		print( match.name1, "won the match", str(p1_score), "-", str(p2_score))
		return match.name1
	else:
		print( match.name2, "won the match", str(p2_score), "-", str(p1_score))
		return match.name2

