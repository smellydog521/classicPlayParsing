# subgraphs are composed of three vetices, and we put weight onto it
# it turns out to be many subgraphs;
# yet we just use none-weighted 13 subgraphs and 
# <ec, bc, strong,weak> to distinguish them

# how to revise into no-edge-sharing

import re,sys,random,os

def subg(edges,lf,sf,sfv,ror):
	# subgraph counts, range from 1 to 13 for 3-node subgraph
	subgraph = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0}
	distinct = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0}
	distinct_weighted = {}
	#twofold = {} # two ingredients come up to <sc,wc>
	
	unit_seq = {}
	unit_seq_sorted = {}
	temp_temp = []

	ec = 0
	#ec_ij = 0 # edge count within subgraph so as to cluster subgraph
	bc = 0
	#bc_ij = 0 # double directed edges count
	sc = 0 #strong count
	wc = 0 #weak count

	unit = {} # key as subgraph, and value as features of subgraph
	fcount = {} # vetex count in the front seat, e.g. A-->B could count as fcount[A]++
	#fcount_ij = {}
	bcount = {} # vetex count in the back seat, e.g. indegree
	#bcount_ij = {}
	score = False 
	bi_boolean = False # for bi-edge check

	#for each connected pair, find a third one connected to either of them
	#better into matrix, but first let just from files
	e_copy = []

	pair = []
	third = 0
	key = ''
	#rpair = ''
	seq = [] # for every subgraph to store all connections 
	#seq_ij = [] # for i,j related conenctions only

	# sort to begin
	edges.sort()

	e_copy = edges

	# motif detection take place in edges and e_copy
	pair = []
	key = ''
	temp = []
	third = 0
	
	for e in edges: # better consider relationship between i,j in inner loop
		# for now, seq_ij has accumulated effect
		# i-->j spotted
		lf.write('We are considering i-->j: <'+e+'>\n')
		for c in e_copy:
			lf.write('\n')
			lf.write('============= New Inner Loop ==============\n')
			lf.write('Inner connection is <'+c+'>\n')
			key = ''
			pair = re.split(',',e)
			seq = []
			ec = 0
			bc = 0
			sc = 0
			wc = 0
			fcount = {}
			bcount = {}
			bi_boolean = False
			score = False

			if c==e:
				continue

			temp = re.split(',',c)
			if temp[1]==pair[0] and temp[0]==pair[1]:# the other edge of biconnection
				continue

			if pair[0] in temp[:-1] or pair[1] in temp[:-1]:# successfully find a triad
				# let's deem 'e' first.
				lf.write('Connections we append: <'+e+'>\n')
				seq.append(e)
				ec = 1
				bc = 0
				fcount[pair[0]] = 1
				bcount[pair[1]] = 1

				#for strong or weak
				if pair[2]=='20':
					sc = sc + 1
				else:
					wc = wc + 1

				# to see if j-->i is applicable
				key = pair[1]+','+pair[0]+',20'
				if key in e_copy:#double edges between i and j
					lf.write('Revise Connections we append: <'+key+'>\n')
					seq.append(key)
					ec = ec + 1
					bc = bc + 1
					sc = sc + 1
					fcount[pair[1]] = 1
					bcount[pair[0]] = 1

				# to see if j-->i is applicable
				key = pair[1]+','+pair[0]+',10'
				if key in e_copy:#double edges between i and j
					lf.write('Revise Connections we append: <'+key+'>\n')
					seq.append(key)
					ec = ec + 1
					bc = bc + 1
					wc = wc + 1
					fcount[pair[1]] = 1
					bcount[pair[0]] = 1
			
				# pick a third one 
				third = 0
				key = ''
			
				# find a subgraph,maybe already did, comprised of pair[0], pair[1] and other in c
				# to find which three
				
				lf.write('We are looking for the third vertex in: '+c+'\n')
				if temp[0] not in pair[:-1]:
					third = temp[0]
				else:
					third = temp[1]
				
				lf.write('The third turns out to be: '+str(third)+'\n')

				# we correct it as:
				temp = []
				temp.append(pair[0])
				temp.append(pair[1])
				temp.append(third)

				temp.sort()
				key = temp[0]+','+temp[1]+','+temp[2]
				#key = str(temp[0])+','+str(temp[1])+','+str(temp[2])

				if key in unit.keys():
					continue

				##### new subgraph found #####
				lf.write('We found a new subgraph: <'+key+'>\n')
				lf.write('@@@@@seq for now we have:@@@@@\n')
				for s in seq:# only pair[0] and pair[1] are involved
					lf.write(s+'\n')
				
				# we got a subgraph now, they are: pair[0], pair[1] and third
				# next, get detail relationships: 
				# they are: pair[0],third; pair[1],third
				# get rid of temp, let's do it from scratch
				k = ''
				for p in pair[:-1]:
					bi_boolean = False
					k = p+','+third+',20'
					if k in e_copy:
						ec = ec + 1
						sc = sc + 1
						bi_boolean = True
						seq.append(k)

						if p in fcount.keys():
							fcount[p] = fcount[p] + 1
						else:
							fcount[p] = 1
						if third in bcount.keys():
							bcount[third] = bcount[third] + 1
						else:
							bcount[third] = 1
					k = p+','+third+',10'
					if k in e_copy:
						ec = ec + 1
						wc = wc + 1
						bi_boolean = True
						seq.append(k)

						if p in fcount.keys():
							fcount[p] = fcount[p] + 1
						else:
							fcount[p] = 1
						if third in bcount.keys():
							bcount[third] = bcount[third] + 1
						else:
							bcount[third] = 1

					k = third+','+p+',20'
					if k in e_copy:
						seq.append(k)
						ec = ec + 1
						sc = sc + 1
						if bi_boolean == True:
							bc = bc + 1
							bi_boolean = False

						if third in fcount.keys():
							fcount[third] = fcount[third] + 1
						else:
							fcount[third] = 1
						if p in bcount.keys():
							bcount[p] = bcount[p] + 1
						else:
							bcount[p] = 1
					k = third+','+p+',10'
					if k in e_copy:
						seq.append(k)
						ec = ec + 1
						wc = wc + 1
						if bi_boolean == True:
							bc = bc + 1
							bi_boolean = False

						if third in fcount.keys():
							fcount[third] = fcount[third] + 1
						else:
							fcount[third] = 1
						if p in bcount.keys():
							bcount[p] = bcount[p] + 1
						else:
							bcount[p] = 1

				lf.write('@@@@@@@@@@Here comes sequences of connections\n')
				for s in seq:
					lf.write(s+'\n')
				lf.write('\n')
				
				# check if ec overflow
				if ec>6:
				    print 'ERROR: ec overflowed!!!'

				# subgraph is about to complete
				# value of unit: count of edges, count of double edges, subgraph-number
				# add ec and bc / 2017.05.14
				unit[key]=str(ec)+','+str(bc)+','+str(sc)+','+str(wc)
				unit_seq[key]=seq
				lf.write('+++++We are copying with '+key+'++++++\n')
				lf.write('We appending following edges:\n')
				lf.write(str(unit_seq[key])+'\n')
				
				# in order to only maitain single edge, we put it into (small edge no, larger edge no) form
				temp = []
				for s in seq:
				    ss = s[:-3] # get rid of ',20' or ',10'
				    first = re.split(',',ss)[0]
				    second = re.split(',',ss)[1]
				    new = second+','+first
				    if first>second and new not in temp:# in alphabet order, not int order
				        temp.append(new)
				    elif ss not in temp:
				        temp.append(ss)
				
				unit_seq_sorted[key]=temp
				temp = []
				lf.write('We appending following binary direction-free edges to unit_seq_sorted as :\n')
				lf.write(str(unit_seq_sorted[key])+'\n')

				# better generate an offset dic from fcount and bcount
				# corresponding offset ==2 would be sign for scatter or assemble

				# begin motif cluster
				if ec==6:
					subgraph[13]=subgraph[13]+1
					unit[key] = unit[key] + ',' + '13'
				elif ec==5:
					subgraph[12]=subgraph[12]+1
					unit[key] = unit[key] + ',' + '12'
				elif ec==4 and bc==2:
					subgraph[8]=subgraph[8]+1
					unit[key] = unit[key] + ',' + '8'
				elif ec==3 and bc==1: # 3 or 7
					# from or to one of the double edged vertex
					# to find the one refered only once in fcount and bcount
					for k in fcount.keys():
						if k not in bcount.keys():
							subgraph[7]=subgraph[7]+1
							unit[key] = unit[key] + ',' + '7'
							break
					for k in bcount.keys():
						if k not in fcount.keys():
							subgraph[3]=subgraph[3]+1
							unit[key] = unit[key] + ',' + '3'
							break
				#else: # that is 2,0 for 124, 3,0 for 59, 4,1 for 61011
					# scatter, together or sequence
				elif ec==2 and bc==0:# 1, 2 or 4
					# two edges only
					score = False
					for k,v in fcount.iteritems():
						if v == 2:
							subgraph[1] = subgraph[1] + 1
							unit[key] = unit[key] + ',' + '1'
							score = True
							break
					for k,v in bcount.iteritems():
						if v == 2:
							subgraph[4] = subgraph[4] + 1
							unit[key] = unit[key] + ',' + '4'
							score = True
							break
					if score==False:
						subgraph[2] = subgraph[2] + 1
						unit[key] = unit[key] + ',' + '2'
				elif ec==3 and bc==0: # 5, 9
					score = False
					for k,v in fcount.iteritems():
						if v == 2:
							subgraph[5] = subgraph[5] + 1
							unit[key] = unit[key] + ',' + '5'
							score = True
							break
					if score==False:
						subgraph[9] = subgraph[9] + 1
						unit[key] = unit[key] + ',' + '9'
				elif ec==4 and bc==1:# 6, 10 and 11
					#bi connection in it
					score = False
					for k,v in fcount.iteritems():
						if v == 2 and k not in bcount.keys():
							subgraph[11] = subgraph[11] + 1
							unit[key] = unit[key] + ',' + '11'
							score = True
							break
					for k,v in bcount.iteritems():
						if v == 2 and k not in fcount.keys():
							subgraph[6] = subgraph[6] + 1
							unit[key] = unit[key] + ',' + '6'
							score = True
							break
					if score==False:
						subgraph[10] = subgraph[10] + 1
						unit[key] = unit[key] + ',' + '10'
				
				#double loop ended

	#print unit
	lf.write('\n')
	lf.write('*********Here comes subgraphs************\n')
	cc = 0
	for k,v in unit.iteritems():
		lf.write(k+':'+v+'\n')
		sfv.write(k+':'+v+':')
		sfv.write(str(unit_seq[k])+'\n')
		cc = cc+1
	lf.write('\n' + str(cc) + ' subgraph count has been written into file.\n')

	# Here we are about to count the distinct number of every single subgraph
	pp = []
	ing_weighted = {} # put ec,bc,sc,wc,sub_no as distinct feature
	ing = {} #only put sub_no as distinct feature
	
	# compute weighted_subgraphs
	# IT IS the true weighted_subgraphs
	weighted_subgraph = {}
	binary_subgraph = {}
	for k, v in unit.iteritems():
		pp = re.split(',',k)
		lf.write('We consider key: '+str(k)+'\n')

		if v not in weighted_subgraph.keys():
			weighted_subgraph[v] = 1
		else:
			weighted_subgraph[v] = weighted_subgraph[v] + 1

		if v not in ing_weighted.keys():
		        distinct_weighted[v] = 1
			ing_weighted[v]=[]
			for edge in unit_seq[k]:
			     ing_weighted[v].append(edge)
			
		else:
		        temp_temp = []
			for edge in unit_seq[k]:
			     if edge not in ing_weighted[v]:
			         temp_temp.append(edge)
			if len(temp_temp)==len(unit_seq[k]):
			     distinct_weighted[v] += 1
			     for edge in temp_temp:
			         ing_weighted[v].append(edge)
		
		vv = int(re.split(',',v)[-1])
		# vv is the exact binary 3 node subgraph no
		if vv not in binary_subgraph.keys():
			binary_subgraph[vv] = 1
		else:
			binary_subgraph[vv] = binary_subgraph[vv] + 1
			
		if vv not in ing.keys():
		        distinct[vv] = 1
			ing[vv]=[]
			for edge in unit_seq_sorted[k]:
			     ing[vv].append(edge)
			
		else:
		        temp_temp = []
			for edge in unit_seq_sorted[k]:
			     if edge not in ing[vv]:
			         temp_temp.append(edge)
			if len(temp_temp)==len(unit_seq_sorted[k]):
			     distinct[vv] += 1
			     for edge in unit_seq_sorted[k]:
			         ing[vv].append(edge)
			
			lf.write('Newly appended a distinct subgraph: \n')
	

	## to count the number of ditinct subgraphs
	## it may not that precise cauz <sc,wc,13_sub> is short for weighted_3_subgraph
	#lf.write('Here comes the distinct version of subgraphs.\n')
	#for k,v in ing.iteritems():
	#	lf.write(str(k)+':'+str(len(v)/3)+'\n')
	#	distinct[k] = len(v)/3
	
	#print subgraph
	#sf.write('\n')
	
	sf.write('Subgraph to be: \n')
	if ror==0:# it is real network
		# write subgraph.txt with distinct no in
		for k,v in weighted_subgraph.iteritems():
		        vv = int(re.split(',',k)[-1])
		        #print vv
		        # weighted subgraph: weighted appearance, distinct count on binary subgraph (1~13): raw appearance, distinct count on weighted subgraph
			sf.write(str(k)+':'+str(v)+','+str(distinct_weighted[k])+':'+str(binary_subgraph[vv])+','+str(distinct[vv])+'\n')
	else: # for randomized network
		for k,v in weighted_subgraph.iteritems():
			sf.write(str(k)+':'+str(v)+'\n')

	unit = {}
	subgraph = {}
	
	
def randomize(edges,single,double,lf,sf,t):
	new_edges = []
	# treat double eges/sigle edges separately
	pair = []
	key = ''
	# set would encounter changed size problem

	ran = [] # target array to store randomized edges
	sran = []
	dran = []
	key1 = ''
	key2 = ''
	key3 = ''
	key4 = ''
	flag = False #sign interpreting if it has been swapped
		
	lf.write('----------------Original edges---------------\n')
	for e in edges:
		lf.write(e+'\t')
	lf.write('\n')

	#print single
	lf.write('\n')
	lf.write('#############Original single edges############\n')
	for s in single:
		lf.write(s+'\t')
	lf.write('\n')
	
	
	#print double
	lf.write('\n')
	lf.write('#############Original double edges#############\n')
	for d in double:
		lf.write(d+'\t')
	lf.write('\n')

	i = ''
	j = ''
	nodesa = []
	nodesb = []
	revi = ''
	sw = '' # strong or weight
	for r in range(t):
		# we can measure the subgraph count within this loop
		# to swap singe edges, given size(single) not changed
		# need to randomize selected edge, set() is not working

		sw = '' # strong or weight

		# ---------for single edges-------------
		while True: # just to gurantee one swap is just happened
			i = random.choice(single)
			j = random.choice(single)

			if i==j:
				continue

			nodesa = re.split(r',',i)
			nodesb = re.split(r',',j)

			if nodesa[0] in nodesb[:-1] or nodesa[1] in nodesb[:-1]:
				continue
			
			# only strong/strong or weak/weak can be swapped
			if nodesa[2]!=nodesb[2]:
				continue

			if nodesa[2]=='10':
				sw = '20'
			else:
				sw = '10'

			lf.write('---------------- begin single loop ----------------\n')
			lf.write('we got four nodes are: '+i+';'+j+'\n')
			lf.write('\n')

			# ready to swap
			key1 = nodesa[0]+','+nodesb[1]+','+nodesa[2]
			key2 = nodesb[0]+','+nodesa[1]+','+nodesa[2]
			key3 = nodesa[0]+','+nodesb[1]+','+sw
			key4 = nodesb[0]+','+nodesa[1]+','+sw

			if key1 not in single and key2 not in single and \
			key1 not in double and key2 not in double and \
			key3 not in single and key4 not in single and \
			key3 not in double and key4 not in double :
				lf.write('************Append randomized single edge: <'+key1+'>************\n')
				single.append(key1)
				lf.write('************Append randomized single edge: <'+key2+'>************\n')
				single.append(key2)

				# expell i and j
				single.remove(i)
				lf.write('************Remove existing single edge: <'+i+'>************\n')
				single.remove(j)
				lf.write('************Remove existing single edge: <'+j+'>************\n')
				lf.write('---------------- end single loop ----------------\n')
				break
		#end of while true

		i = ''
		j = ''
		nodesa = []
		nodesb = []
		key1 = ''
		key2 = ''
		key3 = ''
		key4 = ''
		revi = ''
		revj = ''
		revk = ''
		revl = ''
		sn = {0:0,1:0} # strong count of each set of double edges
		wside = {0:0,1:0}
		sside = {0:0,1:0}
		sw = ''

		# ---------for double edges-------------
		while True:
			i = random.choice(double)
			j = random.choice(double)

			if i==j:
				continue

			nodesa = re.split(r',',i)
			nodesb = re.split(r',',j)

			if nodesa[0] in nodesb[:-1] or nodesa[1] in nodesb[:-1]:
				continue

			if nodesa[2]=='20':
				sn[0]=1
			if nodesb[2]=='20':
				sn[1]=1
			
			# twin edges of i and j
			revi = nodesa[1]+','+nodesa[0]+',10'
			revj = nodesb[1]+','+nodesb[0]+',10'
			revk = nodesa[1]+','+nodesa[0]+',20'
			revl = nodesb[1]+','+nodesb[0]+',20'

			if revk in double:
				sn[0] = sn[0] + 1
			if revl in double:
				sn[1] = sn[1] + 1
			
			# to determine right cases to swap
			# i.e. s/s vs s/s, or ...
			if sn[0]!=sn[1]:
				continue

			lf.write('================== begin double loop =============\n')
			lf.write('we got four nodes are: '+i+';'+j+'\n')
			lf.write('\n')

			if sn[0]==1:# node not equally distributed
				# to determine the weak side of double edges
				if nodesa[2]=='20':
					wside[0] = nodesa[0]
					sside[0] = nodesa[1]
				else:
					wside[0] = nodesa[1]
					sside[0] = nodesa[0]
				
				if nodesb[2]=='20':
					wside[1] = nodesb[0]
					sside[1] = nodesb[1]
				else:
					wside[1] = nodesb[1]
					sside[1] = nodesb[0]

				# ready to swap
				
				key1 = wside[0]+','+sside[1]+',20'
				key2 = wside[1]+','+sside[0]+',20'

				key3 = sside[1]+','+wside[0]+',10'
				key4 = sside[0]+','+wside[1]+',10'

				key11 = wside[0]+','+sside[1]+',10'
				key22 = wside[1]+','+sside[0]+',10'

				key33 = sside[1]+','+wside[0]+',20'
				key44 = sside[0]+','+wside[1]+',20'

				if key1 not in single and key2 not in single and \
				key1 not in double and key2 not in double and \
				key3 not in single and key4 not in single and \
				key3 not in double and key4 not in double and \
				key11 not in single and key22 not in single and \
				key11 not in double and key22 not in double and \
				key33 not in single and key44 not in single and \
				key33 not in double and key44 not in double:
					lf.write('************Append randomized double edge 1: <'+key1+'>************\n')
					double.append(key1)
					lf.write('************Append randomized double edge 2: <'+key2+'>************\n')
					double.append(key2)
					lf.write('************Append randomized double edge 3: <'+key3+'>************\n')
					double.append(key3)
					lf.write('************Append randomized double edge 4: <'+key4+'>************\n')
					double.append(key4)

					# expell i and j
					double.remove(i)
					lf.write('************Remove existing double edge i: <'+i+'>************\n')
					if revi in double:
						double.remove(revi)
						lf.write('************Remove existing double edge revi: <'+revi+'>************\n')
					else:
						double.remove(revk)
						lf.write('************Remove existing double edge revk: <'+revk+'>************\n')
					
					double.remove(j)
					lf.write('************Remove existing double edge j: <'+j+'>************\n')
					if revj in double:
						double.remove(revj)
						lf.write('************Remove existing double edge revj: <'+revj+'>************\n')
					else:
						double.remove(revl)
						lf.write('************Remove existing double edge revl: <'+revl+'>************\n')
					lf.write('=============== end double loop ==============\n')
					break
				

			else:# high/high, low/low encountered
				if nodesa[2]=='10':
					sw = '20'
				else:
					sw = '10'

				# ready to swap
				key1 = nodesa[0]+','+nodesb[1]+','+nodesa[2]
				key2 = nodesb[0]+','+nodesa[1]+','+nodesa[2]

				key3 = nodesb[1]+','+nodesa[0]+','+nodesa[2]
				key4 = nodesa[1]+','+nodesb[0]+','+nodesa[2]

				key11 = nodesa[0]+','+nodesb[1]+','+sw
				key22 = nodesb[0]+','+nodesa[1]+','+sw

				key33 = nodesb[1]+','+nodesa[0]+','+sw
				key44 = nodesa[1]+','+nodesb[0]+','+sw

				if key1 not in single and key2 not in single and \
				key1 not in double and key2 not in double and \
				key3 not in single and key4 not in single and \
				key3 not in double and key4 not in double and \
				key11 not in single and key22 not in single and \
				key11 not in double and key22 not in double and \
				key33 not in single and key44 not in single and \
				key33 not in double and key44 not in double:
					lf.write('************Append randomized double edge 1: <'+key1+'>************\n')
					double.append(key1)
					lf.write('************Append randomized double edge 2: <'+key2+'>************\n')
					double.append(key2)
					lf.write('************Append randomized double edge 3: <'+key3+'>************\n')
					double.append(key3)
					lf.write('************Append randomized double edge 4: <'+key4+'>************\n')
					double.append(key4)

					# expell i and j
					double.remove(i)
					lf.write('************Remove existing double edge i: <'+i+'>************\n')
					if revi in double:
						double.remove(revi)
						lf.write('************Remove existing double edge revi: <'+revi+'>************\n')
					else:
						double.remove(revk)
						lf.write('************Remove existing double edge revk: <'+revk+'>************\n')
					
					double.remove(j)
					lf.write('************Remove existing double edge j: <'+j+'>************\n')
					if revj in double:
						double.remove(revj)
						lf.write('************Remove existing double edge revj: <'+revj+'>************\n')
					else:
						double.remove(revl)
						lf.write('************Remove existing double edge revl: <'+revl+'>************\n')
					lf.write('=============== end double loop ==============\n')
					break
			#end of while true
	#end of for r in range(t)
	

	#print single
	lf.write('\n')
	lf.write('#############Randomized single edges############\n')
	for s in single:
		lf.write(s+'\t')
		new_edges.append(s)
	lf.write('\n')
	
	#print double
	lf.write('\n')
	lf.write('#############Randomized double edges#############\n')
	for d in double:
		lf.write(d+'\t')
		new_edges.append(d)
	lf.write('\n')
	
	# count subgraphs via calling procedure
	lf.write('\n subgraph count begins here.\n')
	
	#print randomized edges
	lf.write('\n')
	lf.write('#############Randomized edges############\n')
	for newe in new_edges:
		lf.write(newe+'\t')
	lf.write('\n')

	# call subg to count subgraphs
	subg(new_edges,lf,sf,1)
	
def main(argv):
	# give the gross number to be swapped before fully randomized
	N = 10
	# give the number of randomized network
	M = 100
	# to store edges from file
	edges = []
	single = []
	double = []
	key1 = ''
	key2 = ''
	pair = []
	rf = ''
	f = ''
	log_file = ''
	#log_file_random = ''
	subgraph_file = ''
	subgraph_file_verbose=''
	line = ''

	for parents,dirnames,filenames in os.walk(argv[1]):
		for fn in filenames:
			if '_edges.txt' in fn:
				print '------Begin Processing '+fn+'--------'
				edges = []
				single = []
				double = []
				key1 = ''
				key2 = ''
				line = ''

				rf = open(argv[1]+'/'+fn,'r')
				f = open(argv[1]+'/'+fn[:fn.index('_')]+'_weighted_3_node_simple.txt','w+')
				log_file = open(argv[1]+'/'+fn[:fn.index('_')]+'_weighted_3_node_log.txt','w')
				#log_file_random = open(argv[1]+'/'+fn[:str(fn).index('_')]+'_weighted_3_node_random_log.txt','w')
				subgraph_file = open(argv[1]+'/'+fn[:str(fn).index('_')]+'_weighted_3_node_subgraph.txt','w+')
				subgraph_file_verbose = open(argv[1]+'/'+fn[:str(fn).index('_')]+'_weighted_3_node_subgraph_verbose.txt','w+')
				
				
				for line in rf:
					if('Source' in line):
						continue
					line = line[:line.index(',D')]+line[line.index('d,')+1:] # weight is considered here
					f.write(line)
				
				#into set
				f.seek(0)
				for line in f:
					pair = re.split(',',line[:-1])
					key = pair[0]+','+pair[1]+','+pair[2]
					edges.append(key)
				
				edges.sort()

				key1 = ''
				key2 = ''
				# to cluster into single or double
				for e in edges:
					# to see if reverse ege exists
					pair = re.split(',',e)
					key1 = pair[1]+','+pair[0]+',10'
					key2 = pair[1]+','+pair[0]+',20'
					if key1 not in edges and key2 not in edges:
						single.append(e)
					else:# either edge of double correlations are included in 'double'
						double.append(e)
						# double.append(key)
				
				#print 'total edge count:'+str(len(edges))
				#print 'single edge count:'+str(len(single))
				#print 'double edge count:'+str(len(double))

				if len(double)%2!=0:
					print str(len(double)) + '--Double is not DOUBLE!\n'
				
				# call to find subgraphs
				# for original network
				subg(edges,log_file,subgraph_file,subgraph_file_verbose,0)
				# for randomized network
				#for m in range(M):
				#	randomize(edges,single,double,log_file_random,subgraph_file,len(edges))# motif detection
				print '======End Processing '+fn+'======'
if __name__ == '__main__':
    main(sys.argv)
