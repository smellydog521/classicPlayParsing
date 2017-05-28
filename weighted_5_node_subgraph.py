# we are here to get weighted-5-node-subgraph, 
# given edge-count/bi-edge-count/strong-tie-count/weak-tie-count only to distinguish
# to leverage on weighte 4 node subgraphs(edge_count, biedge_count, strong_count, weak_count, subNo)
# next to share not edge

import re,sys,random, os

def subg(edges,s4,lf,sf,sfv,ror):
	# subgraph counts, range from 1 to 13 for 3-node subgraph
	#subgraph = {}
	distinct = {}
	ec = 0
	#ec_ij = 0 # edge count within subgraph so as to cluster subgraph
	bc = 0
	#bc_ij = 0 # double directed edges count
	sc = 0
	wc = 0
	unit = {} # key as subgraph, and value as features of subgraph
	fcount = {} # vetex count in the front seat
	#fcount_ij = {}
	bcount = {} # vetex count in the back seat
	#bcount_ij = {}
	bi_boolean = False # for bi-edge check

	pair = []
	temp = []
	third = 0
	key = ''
	#rpair = ''
	seq = [] # for every subgraph to store all connections 
	#seq_ij = [] # for i,j related conenctions only

	# sort to begin
	edges.sort()
	
	unit_seq = {}
	unit_seq_sorted = {}

	# motif detection take place in edges and e_copy
	pair = []
	key = ''
	temp = []
	nodes = []
	features = []
	new = ''
	sub_can = []
	
	for sub in s4: # strong edge count, weak edge count, and sub-no, giving #13 at most
	        #lf.write('')
		
		lf.write('We are considering 4 node subgraph: <'+sub+'>\n')
		for c in edges:
		        nodes = re.split(',',re.split(':',sub)[0])
		        features = re.split(',',re.split(':',sub)[1])
		        sub_can = re.split('\'',re.split(':',sub)[2][1:-1])
			lf.write('\n')
			lf.write('============= New Inner Loop ==============\n')
			lf.write('Innner connection is <'+c+'>\n')
			key = ''
			temp = re.split(',',c)
			
			if temp[0] in nodes and temp[1] in nodes or \
			temp[0] not in nodes and temp[1] not in nodes:
			    continue
			
			if temp[0] not in nodes:
			    new = temp[0]
			    nodes.append(new)
			else:
			    new = temp[1]
			    nodes.append(new)
			    
			nodes.sort()
			key = nodes[0]+','+nodes[1]+','+nodes[2]+','+nodes[3]+','+nodes[4]

			if key in unit.keys():
				continue
				
		        # to see new to other's connection
			ec = int(features[0])
			bc = int(features[1])
			sc = int(features[2])
			wc = int(features[3])
			#fcount = {}
			#bcount = {}
			bi_boolean = False
			
			seq = []
			### Get edges from this 4-node-subgraph ###
			for x in sub_can:
			    if len(x)<4:
			        continue
			    seq.append(x)

			##### new subgraph found #####
			lf.write('We found a new 5_node_subgraph: <'+key+'>\n')
			lf.write('@@@@@seq for now we have:@@@@@\n')
			for s in seq:
				lf.write(s+'\n')
			
			# we got a subgraph now, they are e and c
			# next, get detail relationships across e and c
			k = ''
			for n in nodes:
				if n!=new:
					bi_boolean = False
					k = n+','+new+',20'
					if k in edges:
						ec += 1
						sc += 1
						bi_boolean = True
						seq.append(k)
#
#						if p in fcount.keys():
#							fcount[p] = fcount[p] + 1
#						else:
#							fcount[p] = 1
#						if third in bcount.keys():
#							bcount[third] = bcount[third] + 1
#						else:
#							bcount[third] = 1

					k = n+','+new+',10'
					if k in edges:
						ec = ec + 1
						wc = wc + 1
						bi_boolean = True
						seq.append(k)

					k = new+','+n+',20'
					if k in edges:
						seq.append(k)
						ec = ec + 1
						sc = sc + 1
						if bi_boolean == True:
							bc = bc + 1
							bi_boolean = False

					k = new+','+n+',10'
					if k in edges:
						seq.append(k)
						ec = ec + 1
						sc = sc + 1
						if bi_boolean == True:
							bc = bc + 1
							bi_boolean = False

			#lf.write('@@@@@@@@@@Here comes sequences of connections\n')
			#for s in seq:
			#	lf.write(s+'\n')
			#lf.write('\n')
                        
                        # check if ec overflow
			if ec>20:
 			        print 'ERROR: ec overflowed!!!'+str(ec)
 			        lf.write('ERROR: ec overflowed!!!'+str(ec)+'\n')
				    
			# subgraph is about to complete
			# value of unit:
			unit[key]=str(ec)+','+str(bc)+','+str(sc)+','+str(wc)
			unit_seq[key]=seq
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
		#double loop ended

	#print unit
	lf.write('\n')
	lf.write('*********Here comes subgraphs************\n')
	c = 0
	for k,v in unit.iteritems():
		lf.write(k+':'+v+'\n')
		sfv.write(k+':'+v+':')
		sfv.write(str(unit_seq[k])+'\n')
		c = c+1
	lf.write('\n' + str(c) + ' subgraph count has been written into file.\n')

	# Here we are about to count the distinct number of every single subgraph
	pp = []
	ing_weighted = {} # put ec,bc,sc,wc,sub_no as distinct feature
	ing = {} #only put sub_no as distinct feature
	
	# compute weighted_subgraphs
	# IT IS the true weighted_subgraphs
	weighted_subgraph = {}
	binary_subgraph = {}
	distinct_weighted = {}
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

	# to count the number of ditinct subgraphs
	# it may not that precise cauz <sc,wc,13_sub> is short for weighted_3_subgraph
	#lf.write('Here comes the distinct version of subgraphs.\n')
	#for k,v in ing.iteritems():
	#	lf.write(str(k)+':'+str(len(v)/4)+'\n')
	#	distinct[k] = len(v)/4
	
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
	else:
		for k,v in weighted_subgraph.iteritems():
			sf.write(str(k)+':'+str(v)+'\n')
	
def main(argv):
	# to store edges from file
	edges = []
	subgraph_of_4_node = []
        subgraph_file_verbose =''
       	pair = []
	rf = ''
	f = ''
	log_file = ''
	#log_file_random = ''
	subgraph_file = ''
	line = ''
        sub4 = ''

	for parents,dirnames,filenames in os.walk(argv[1]):
		for fn in filenames:
			if '_edges.txt' in fn:
				print '------Begin Processing '+fn+'--------'
				edges = []
				subgraph_of_4_node = []
				line = ''

				rf = open(argv[1]+'/'+fn,'r')
				sub4 = open(argv[1]+'/'+fn[:fn.index('_')]+'_weighted_4_node_subgraph_verbose.txt','r')
				f = open(argv[1]+'/'+fn[:fn.index('_')]+'_weighted_5_node_simple.txt','w+')
				log_file = open(argv[1]+'/'+fn[:fn.index('_')]+'_weighted_5_node_log.txt','w')
				#log_file_random = open(argv[1]+'/'+fn[:str(fn).index('_')]+'_weighted_4_node_random_log.txt','w')
				subgraph_file = open(argv[1]+'/'+fn[:str(fn).index('_')]+'_weighted_5_node_subgraph.txt','w+')
				subgraph_file_verbose = open(argv[1]+'/'+fn[:str(fn).index('_')]+'_weighted_5_node_subgraph_verbose.txt','w+')
				#get 3_node_subgraphs
				for line in sub4:
				    subgraph_of_4_node.append(line.strip())
				
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

				# call to find subgraphs
				# for original network
				subg(edges,subgraph_of_4_node, log_file,subgraph_file,subgraph_file_verbose,0)
				# for randomized network
				#for m in range(M):
				#	randomize(edges,single,double,log_file_random,subgraph_file,len(edges))# motif detection
				print '======End Processing '+fn+'======'

if __name__ == '__main__':
    main(sys.argv)
