###########################################################################################	
###########################################################################################	
###########################################################################################	
def Professor(sbj,candidates,period,profPos,candOrdered,profPeriod,force):
	#print("Position:",profPos,"\nSubject:",sbj,"\nforce =",force,"\nNumber of candidates:",len(candOrdered))
	got = 0
	while(got==0):
		if(len(candOrdered)==profPos and force == 0): profPos = 0; force = 1
		elif(len(candOrdered)==profPos and force == 1): raise Exception("No professor is able to teach the requested subject")
		else: pass
		if(profPeriod[candOrdered[profPos][1]][period]==2 or force==1):
			professor = candOrdered[profPos][1]
			got = 1
		else:
			profPos += 1
		
	return professor, profPos, force

###########################################################################################	
###########################################################################################	
###########################################################################################	
def Neighborhood(sbjHPW, sbjGroups, sbjBook, profBook, profSche, profSubject, profPeriod):

	#from math import *
	import copy

	neighborhood = []
	for i in range(len(sbjGroups)): # Make one permutation for each subject group
		for j in range(5): # Each group has 5 subjects
			sbj1 = sbjGroups[i][j] # Get the current subject number
			hpw1 = sbjHPW[sbj1] # Get hours per week
			s1 = int(hpw1/2)+hpw1%2 # Get number of slots that this subject requires
			for k in range(s1):
				for l in range(len(sbjBook[sbj1])):
					prof1 = sbjBook[sbj1][l][3] # Get the professor number
					info1 = sbjBook[sbj1][l] # Get the subject info (info = [subject,period,hpw,professor,group,slot,slot2,slot3])
					period1 = info1[1]
					current1 = info1[5+k]
					if(k+1!=s1 or hpw1%2==0): cs1 = 2
					else: cs1 = 1
					for m in range(6): # The destination can be being occupied by any of the groups' subject, even the same subject which is being moved or not being occupied
						if(m==5):
							sbj2 = -1
							hpw2 = 2
							s2 = 1
						else:
							sbj2 = sbjGroups[i][m]
							hpw2 = sbjHPW[sbj2]
							s2 = int(hpw2/2)+hpw2%2
						for n in range(len(sbjBook[sbj2])):
							prof2 = sbjBook[sbj2][n][3] # Get the professor number
							info2 = sbjBook[sbj2][n] # Get the subject info (info = [subject,period,hpw,professor,group,slot,slot2,slot3])
							period2 = info2[1]
							for o in range(s2):
								current2 = info2[5+o]
								if(o+1!=s2 or hpw2%2==0): cs2 = 2
								else: cs2 = 1
								if(i==info1[4]==info2[4] and period1==period2 and info1!=info2):
									if(prof2==-1 and profSche[prof1][period1][current2]<=int(k+1/s1)*hpw1%2):
										permute = 1
									elif((cs1==cs2 or (cs1==1 and profSche[prof1][period1][current1]==1) or (cs2==1 and profSche[prof2][period2][current2]==1)) and (profSche[prof1][period1][current2]+cs2 <= 2 and profSche[prof2][period2][current1]+cs1 <= 2) and ((profSche[prof1][period1][current2]<=0+int((k+1)/s1)*hpw1%2 and profSche[prof2][period2][current1]<=0+int((o+1)/s2)*hpw2%2) or prof1==prof2)):
										permute = 1
									else:
										permute = 0
									if(permute==1):
										new_info1 = copy.deepcopy(info1)
										new_info1[5+k] = current2
										new_info2 = copy.deepcopy(info2)
										new_info2[5+o] = current1
										cost = Cost(info1,info2,new_info1,new_info2,profSche,profSubject,profPeriod,sbjBook)
										neighbor = (info1,info2,new_info1,new_info2,cost)
										if(neighbor in neighborhood): pass
										else: neighborhood.append(neighbor)
										if(info1[4]!=info2[4]): print("Error! Permutation being made between different subject groups!")
										elif(info1[1]!=info2[1]): print("Error! Permutation being made between different periods!")
									else: pass

	for i in sbjBook: # Make permutations for subjects that are outside subject groups
		for j in range(len(sbjBook[i])):
			info = sbjBook[i][j]
			professor = info[3]
			sbj = info[0]
			period = info[1]
			hpw = info[2]
			for k in range(len(info)-5):
				from_slot = info[5+k]
				if(info[4]==None and info[0]!=-1): # This subject isn't in any subject group and it is actually being offered
					for l in range(10): # iterate for all the slots
						if((profSche[professor][period][l]==0 or (profSche[professor][period][l]==1 and (hpw%2==1 and k+6==len(info)))) and from_slot!=l):
							#print(l,profSche[professor][period],profSche[professor][period][l])
							new_info = copy.deepcopy(info)
							new_info[5+k] = l
							ghost_info = [-1,period,2,-1,None,l]
							new_ghost_info = [-1,period,2,-1,None,from_slot]
							cost = Cost(info,ghost_info,new_info,new_ghost_info,profSche,profSubject,profPeriod,sbjBook)
							neighbor = (info,ghost_info,new_info,new_ghost_info,cost)
							if(neighbor in neighborhood): pass
							else: neighborhood.append(neighbor)
							#print('\nHEY\n',info,ghost_info,'\n',new_info,ghost_info,'\n')
						else: pass

	# Subject and period preferences movements, i.e. professor exchanges
	for i in sbjBook:
		for j in range(len(sbjBook[i])):
			info = sbjBook[i][j]
			professor = info[3]
			sbj = info[0]
			period = info[1]
			hpw = info[2]
			group = info[4]
			schedule = profSche[professor]
			sbj_slots = []
			for k in range(len(info)-5):
				sbj_slots.append(info[5+k])
			for k in sbjBook:
				for l in range(len(sbjBook[k])):
					info2 = sbjBook[k][l]
					professor2 = info2[3]
					sbj2 = info2[0]
					period2 = info2[1]
					hpw2 = info2[2]
					group2 = info2[4]
					schedule2 = profSche[professor2]
					sbj2_slots = []
					for m in range(len(info2)-5):
						sbj2_slots.append(info2[5+m])
					# professor exchange
					if(professor==professor2 or professor==-1 or professor2==-1): pass
					else:
						if(sbj in profSubject[professor2] and sbj2 in profSubject[professor]):
							count = 0
							for m in sbj2_slots:
								count += 1
								if(schedule[period2][m]==0 or (m in sbj_slots and period==period2 and (not(count==len(info2)-5 and hpw2%2==1) or ((count==len(info2)-5 and hpw2%2==1) and ( hpw%2==1 and info[-1]==m )))) or (schedule[period2][m]==1 and count==len(info2)-5 and hpw2%2==1)):
									try: permute
									except: permute = 1
								else: permute = 0
							count = 0
							for n in sbj_slots:
								count += 1
								if(schedule2[period][n]==0 or (n in sbj2_slots and period==period2 and (not(count==len(info)-5 and hpw%2==1) or ((count==len(info)-5 and hpw%2==1) and ( hpw2%2==1 and info2[-1]==n )))) or (schedule2[period][n]==1 and count==len(info)-5 and hpw%2==1)):
									try: permute
									except: permute = 1
								else: permute = 0
							if(sbj==sbj2 and period==period2): permute = 0
							else: pass
							if(permute==1):
								new_info2 = copy.deepcopy(info)
								new_info2[3] = professor2
								new_info = copy.deepcopy(info2)
								new_info[3] = professor
								cost = Cost(info,info2,new_info,new_info2,profSche,profSubject,profPeriod,sbjBook)
								neighbor = (info,info2,new_info,new_info2,cost)
								if(neighbor in neighborhood): pass
								else: neighborhood.append(neighbor)#; print('HAHA',neighbor)
							else: pass

	return neighborhood
	
###########################################################################################	
###########################################################################################	
###########################################################################################	
def Neighborhood_refactored(sbjHPW, sbjGroups, sbjBook, profBook, profSche, profSubject, profPeriod):

	import copy

	neighborhood = []
	for subject in sbjBook:
		for info in sbjBook[subject]:
			professor = info[3]
			period = info[1]
			hpw = info[2]
			group = info[4]
			slots_to_go = [i for i in range(10) if(i not in info[5:])]
			for from_slot in info[:5]:
				if(fromslot==info[-1] and hpw%2==1): required_space = 1
				else: required_space = 2
				for to_slot in slots_to_go:
					destination_infos = []
					occupied_space1 = 0
					occupied_space2 = 0
					good_to_go = True
					# Verify destination slot in professor's schedule
					for other_info in profBook[perofessor]:
						if(other_info[1]==period and to_slot in other_info[5:]):
							if(slot==other_info[-1] and other_info[2]%2==1): occupied_space1 += 1
							else: occupied_space1 += 2
							if(other_info not in destination_infos): destination_infos.append(other_info)
							else: pass
							if(occupied_space1==2): break
							else: pass
						else: pass
					# Verify destination slot in group's schedule
					for group_subject in sbjGroups[group]:
						for other_info in sbjBook[group_subject]:
							if(other_info[1]==period and slot in other_info[5:]):
								if(other_info[3]!=professor):
									if(slot==other_info[-1] and other_info[2]%2==1): occupied_space2 += 1
									else: occupied_space2 += 2
								else: pass
								if(2-occupied_space2>=required_space): pass
								else: good_to_go = False
							else: pass
					if(good_to_go==True):
						
					else: pass



			
	
	return neighborhood

###########################################################################################
###########################################################################################	
###########################################################################################		
def Cost(orig1, orig2, move1, move2, profSche, profSubject, profPeriod, sbjBook):

	import itertools
	import copy

	hypothetical_sbjBook = copy.deepcopy(sbjBook)
	for orig in (orig1,orig2):
		sbj = orig[0]
		if(sbj!=-1): hypothetical_sbjBook[sbj].remove(orig)
		else: pass
	for move in (move1,move2):
		sbj = move[0]
		if(sbj!=-1): hypothetical_sbjBook[sbj].append(move)
		else: pass
		
	cost = 0
	for i,j in (move1,orig1),(move2,orig2):
	
		sbj = i[0]
		osbj = j[0]
		prof = i[3]
		period = i[1]
		operiod = j[1]
		hpw = i[2]
		ohpw = j[2]
		sche = copy.deepcopy(profSche[prof])
		osche = profSche[prof]
		
		try:
			for k in range(3):
				sche[operiod][j[5+k]] -= 2
		except:
			if(ohpw%2==1): sche[operiod][j[4+k]] += 1
			else: pass
		try:
			for k in range(3):
				sche[period][i[5+k]] += 2
		except:
			if(hpw%2==1): sche[period][i[4+k]] -= 1
			else: pass
		
		if(orig1[3]!=orig2[3]):
			if(i[3]==-1): pass
			else:	
				
				# Subject preference satisfaction
				#-----Movement-----#
				if(profSubject[prof][0]==sbj): pass
				elif(profSubject[prof][1]==sbj): cost += 1
				elif(profSubject[prof][2]==sbj): cost += 2
				else: cost += 3
				#-----Original-----#
				if(profSubject[prof][0]==osbj): pass
				elif(profSubject[prof][1]==osbj): cost -= 1
				elif(profSubject[prof][2]==osbj): cost -= 2
				else: cost -= 3
				# Period preference satisfaction
				#-----Movement-----#
				if(profPeriod[prof][period]==2): pass
				else: cost += 3
				#-----Original-----#
				if(profPeriod[prof][operiod]==2): pass
				else: cost -= 3
		else: pass
				
		# Compactness of the schedule
		#-----Movement-----#
		day = []
		for k in range(5):
			day.append([])
			for l in range(3):
				day[k].append(sche[l][0+2*k]) # Add slots from 0 to 9 for each period of the day,
				day[k].append(sche[l][1+2*k]) # each pair of slots represents a week day (e.g. [0,1] = Monday, [2,3] = Tuesday, etc.)
				if(sche[l][0+2*k]!=0 or sche[l][1+2*k]!=0): cost += 1 # Each day the professor have to go to the university has a cost of 1
				else: pass
		for k in range(5):
			for l in range(6):
				try:
					if(day[k][l]!=0 and (day[k][l-1]!=0 or day[k][l+1]!=0)): cost += 1 # If there isn't a class after or before one class it adds up 1 in cost as penalty for descontinuity
					elif(day[k][l]==0 and day[k][l-1]!=0 and day[k][l+1]!=0): cost += 2 # If there is a hole in the schedule it adds up 2 in cost as penalty for waste of time
					elif(day[k][l]!=0 and day[k][l-1]==0 and day[k][l+1]==0): cost += 3 # If there is a class isolated in the schedule it adds up 3 in cost as penalty for double waste
					else: pass # If there are classes before and after one class no penalty is given as the schedule is continuous
				except:
					try:
						if(day[k][l]!=0 and day[k][l+1]==0): cost += 3 # If there is a class at 8 am and there is no class at 10 am it adds up 3 in cost as penalty for double waste
						else: pass
					except:
						if(day[k][l]!=0 and day[k][l-1]==0): cost += 3 # If there is a class at 9 pm and there is no class at 7 pm it adds up 3 in cost as penalty for double waste
						else: pass
		#-----Original-----#
		day = []
		for k in range(5):
			day.append([])
			for l in range(3):
				day[k].append(osche[l][0+2*k])
				day[k].append(osche[l][1+2*k])
				if(osche[l][0+2*k]!=0 or osche[l][1+2*k]!=0): cost -= 1
				else: pass
		for k in range(5):
			for l in range(6):
				try:
					if(day[k][l]!=0 and (day[k][l-1]!=0 or day[k][l+1]!=0)): cost -= 1
					elif(day[k][l]==0 and day[k][l-1]!=0 and day[k][l+1]!=0): cost -= 2
					elif(day[k][l]!=0 and day[k][l-1]==0 and day[k][l+1]==0): cost -= 3
					else: pass
				except:
					try:
						if(day[k][l]!=0 and day[k][l+1]==0): cost -= 3
						else: pass
					except:
						if(day[k][l]!=0 and day[k][l-1]==0): cost -= 3
						else: pass
		
		# Organization of the schedule
		#-----Movement-----#
		for pair in itertools.combinations(i[5:],2):
			if(pair[0]==pair[1]+1-2*(pair[0]%2)): cost += 2 # If there are two classes of the same subject for the same class in a row it adds up 2 in cost as penalty for too long class
			elif(pair[0]==pair[1]+5-2*(pair[0]%2) or pair[0]==pair[1]-3-2*(pair[0]%2)): pass # If the classes of a subject are alternated there is no penalty as it is good organization
			else: cost += 1 # If the classes are not alternated it adds up 1 in cost as penalty for not so good organization
		for subject in hypothetical_sbjBook:
			if(subject == -1): pass
			else:
				record = [[],[],[]]
				for classroom in hypothetical_sbjBook[subject]:
					period = classroom[1]
					schedule = classroom[5:]
					if(schedule not in record[period]):
						record[period].append(schedule)
					else: pass
				for period in range(3):
					for classes in itertools.combinations(record[period],2):
						for slot1 in classes[0][1:]:
							for slot2 in classes[1][1:]:
								if(slot1==slot2+1-2*(slot1%2)): break
								else: pass
							else: cost += 2
		
		
		#-----Original-----#
		for pair in itertools.combinations(j[5:],2):
			if(pair[0]==pair[1]+1-2*(pair[0]%2)): cost -= 2 # If there are two classes of the same subject for the same class in a row it adds up 2 in cost as penalty for too long class
			elif(pair[0]==pair[1]+5-2*(pair[0]%2) or pair[0]==pair[1]-3-2*(pair[0]%2)): pass # If the classes of a subject are alternated there is no penalty as it is good organization
			else: cost -= 1 # If the classes are not alternated it adds up 1 in cost as penalty for not so good organization
		for subject in sbjBook:
			if(subject == -1): pass
			else:
				record = [[],[],[]]
				for classroom in sbjBook[subject]:
					period = classroom[1]
					schedule = classroom[5:]
					if(schedule not in record[period]):
						record[period].append(schedule)
					else: pass
				for period in range(3):
					for classes in itertools.combinations(record[period],2):
						for slot1 in classes[0][1:]:
							for slot2 in classes[1][1:]:
								if(slot1==slot2+1-2*(slot1%2)): break
								else: pass
							else: cost -= 2
		
	return cost
	
###########################################################################################
###########################################################################################
###########################################################################################
def Best(BestIter, rejected, T, Ti, sbjHPW, sbjGroups, sbjBook, profBook, profSche, profSubject, profPeriod, global_best, liquid_cost):
	
	N = Neighborhood(sbjHPW, sbjGroups, sbjBook, profBook, profSche, profSubject, profPeriod)
	index = [None,None]
	addforward = 0
	bypass = 0
	lowest = 10**10
	
	for i in range(len(N)):
		if(N[i][-1] < lowest and N[i] not in rejected):
			BestMove = N[i]
			lowest = N[i][-1]
		else: pass
	
	for i in range(2):
		if(BestMove[0+i]==BestMove[2+i]):
			bypass += 1
		else:
			for j in range(8):
				if(BestMove[0+i][j]!=BestMove[2+i][j]):
					index[i] = j
					break
				else: pass
	if(len(T)>7):
		del T[0]
		del Ti[0]
	else: pass
	for i in (2,3):
		if(BestMove[i] in T):
			pos = [y for y,x in enumerate(T) if x == BestMove[i]]
			pos = pos[0]
			if(index[i-2]==Ti[pos] and not liquid_cost + lowest < global_best): bypass = 0
			else: bypass += 1
		else: bypass += 1
	
	if(bypass > 0):
		T.append(BestMove[2])
		T.append(BestMove[3])
		Ti.append(index[0])
		Ti.append(index[1])
		liquid_cost += lowest
		if(liquid_cost < global_best):
			global_best = liquid_cost
			BestIter += 1
		else: pass
	else:
		rejected.append(BestMove)
		BestMove, BestIter, global_best, liquid_cost = Best(BestIter, rejected, T, Ti, sbjHPW, sbjGroups, sbjBook, profBook, profSche, profSubject, profPeriod, global_best, liquid_cost)

	return BestMove, BestIter, global_best, liquid_cost

###########################################################################################
###########################################################################################
###########################################################################################
def InitialSolution(p, profPeriod, profSubject, sbjPeriod, sbjHPW, sbjOrdered, sbjGroups, sbjProfs):

	import copy
	
	import assign

	# Create empty lists and dictionaries
	candAval = []
	profSche = []
	for i in range(p):
		profSche.append([[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]])

	# Obtain an avaliation of the possibility of each professor for teaching a certain subject
	for i in range(len(sbjGroups)): # make the avalitaion for subjects into subject groups
		for j in range(5): # each group has 5 subjects
			sbj = sbjGroups[i][j] # get current subject number
			candidates = sbjProfs[i] # get the list of candidates for teaching this subject
			groupAval = []
			for k in range(len(candidates)):
				aval = 0 # starting score is 0, maximum score is 5
				if(sbjPeriod[sbj]==1 and (profPeriod[candidates[k][0]][0]==2 and profPeriod[candidates[k][0]][2]!=2)): aval += 1 # 1 point if period is partially matching
				elif(sbjPeriod[sbj]==1 and (profPeriod[candidates[k][0]][2]==2 and profPeriod[candidates[k][0]][0]!=2)): aval += 1
				elif(sbjPeriod[sbj]==1 and (profPeriod[candidates[k][0]][0]==2 and profPeriod[candidates[k][0]][2]==2)): aval += 2 # 2 points for exact period matching
				elif(sbjPeriod[sbj]==2 and profPeriod[candidates[k][0]][1]==2): aval += 2
				elif(profPeriod[candidates[k][0]][0]==profPeriod[candidates[k][0]][1]==profPeriod[candidates[k][0]][2]): aval += 1
				else: pass
				aval += 3-candidates[k][1]
				groupAval.append([aval,candidates[k][0]]) # store avaliation of this professor in this subject group
			candAval.append(groupAval) # store the avaliation of all professors in all subject groups

	candOrdered, sbjBook, profBook, profSche = assign.SubjectsToProfessors_refactored(p, candAval, profSche, profPeriod, profSubject, sbjPeriod, sbjHPW, sbjOrdered, sbjGroups, sbjProfs)

	# Save initial solution
	
	sbjBook0 = copy.deepcopy(sbjBook)
	profBook0 = copy.deepcopy(profBook)
	profSche0 = copy.deepcopy(profSche)

	return candAval, profSche, sbjBook0, profBook0, profSche0, candOrdered, sbjBook, profBook, profSche
