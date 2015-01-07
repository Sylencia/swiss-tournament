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