# Just ? and To Sb. are considered
# regular expression
import re,sys

def preprocessing(f,sf,logg):
	excep = ['ALL','All','all','BOTH','Both','both','AND','And','and','BUT','But','but', ',']
	stage = set()
	nodes = []
	temp_file = open('temp.xml','w+')
	coun = 0 # to determine if no one is specified after exit
	last_guy = ''

	# parse characters as nodes
	f.seek(0)
	for line in f:
		if '<a name=\"speech' in line or '<A NAME=speech' in line:
			protagonist = line[line.index('<b>')+3:line.index('</b>')].strip()
			if 'but' in protagonist:
				protagonist = protagonist[:protagonist.index('but')]
			protagonist = re.sub(r'and ','',protagonist).strip()
			protagonist = re.sub(r',',' ',protagonist).strip()
			if len(set(protagonist.split(' ')).intersection(set(excep)))==0:
				protagonist = re.sub(r' ',r'_',protagonist).strip()
				if protagonist not in nodes:
					nodes.append(protagonist)
			# space within character is substition replaced by underscore
			line = line[:line.index('<b>')+3]+protagonist+line[line.index('</b>'):]
		temp_file.write(line)
	
	# parse stage 
	f.seek(0)
	temp_file.seek(0)
	for no,line in enumerate(temp_file):
		if '<i>' in line and ('Enter' in line or 'enter' in line):# include Re-enter
		      # line ends with \n, which would not interrupt <i>...</i>
		      # safely to filter with if '</i>' in line:
			words = line[line.index('<i>')+3:line.index('</i>')]
			# substitute anything other than identifier, i.e. \W
			words = re.sub('^0-9a-zA-Z_',' ',words).strip()
			for w in words.split(' '):
				if w in nodes and w not in stage:# A' wife, witches
					stage.add(w)
					logg.write(str(no+1)+' -Enter- : '+w+'\n')

		if '<i>' in line and \
		('Exit' in line or 'Exeunt' in line or 'exit' in line or 'exeunt' in line or 'Dies' in line or 'dies' in line):# Exeunt A and/, B; Exit all; Exeunt all witches
			if 'Exit' in line:
				e = 'Exit'
			elif 'exit' in line:
				e = 'exit'
			elif 'Exeunt' in line:
				e = 'Exeunt'
			elif 'exeunt' in line:
				e = 'exeunt'
			elif 'Dies' in line:
				e = 'Dies'
			elif 'dies' in line:
				e = 'dies'
			
			# For examples like 'Exit all witches', 'Exeunt both murderers'
			# TO DO
			if line[line.index(e)+len(e)]==' ': # Not exit/exeunt alone
				exit_people = line[line.index(e)+len(e):line.index('</i>')].strip()
				exit_people = re.sub(r'[,.?!;]',' ',exit_people).strip()
				exit_people = re.sub(r'and ',' ',exit_people).strip()
				if 'but' in exit_people:
					exit_people = exit_people[:exit_people.index('but')]
				if 'except' in exit_people:
					exit_people = exit_people[:exit_people.index('except')]
				for n in exit_people.split(' '):
					if n in stage:
						stage.remove(n)

			elif e=='Exeunt' or e=='exeunt': # exit all
				stage.clear()
				logg.write(str(no+1)+' -Exeunt: Clear Stage- : '+'\n')
			elif (e=='Exit' or e=='exit' or e=='Dies' or e=='dies') and last_guy!='':
				stage.remove(last_guy)
			
		if 'SCENE' in line or 'Scene' in line:
			last_guy = ''
			stage.clear()
			logg.write(str(no+1)+' -SCENE: Clear Stage- : '+'\n')

		if '[Aside to' in line:
			t = '[Aside to'
			line = line[:line.index(t)+1]+'To'+line[line.index(t)+9:]
		if '<a name=\"speech' in line or '<A NAME=speech' in line:# To check if someone is not explicitely narrated in enter line
			protagonist = line[line.index('<b>')+3:line.index('</b>')].strip()
			# Tackle 'ALL' and 'BOTH'
			if 'ALL' in protagonist or 'All' in protagonist or 'BOTH' in protagonist or 'Both' in protagonist: # Both murderers, All witches
				if 'ALL' in line:
					a = 'ALL'
				elif 'All' in line:
					a = 'All'
				elif 'BOTH' in line:
					a = 'BOTH'
				elif 'Both' in line:
					a = 'Both'
				
				if ' ' in protagonist: # group members like 'All witches'
					protagonist = protagonist[len(a)+1:].strip()
					new_p = ''
					for s in stage:
						if (s[0]==protagonist[0] or s[0].lower()==protagonist[0]) and s[1:-2]==protagonist[1:-2]:
							new_p = new_p + ' ' + s
					protagonist = new_p.strip()

				else: # solo word like ALL, BOTH
					protagonist = re.sub(a,' ',protagonist).strip()
					protagonist = re.sub(r',',' ',protagonist).strip()
					for s in stage:
						protagonist = protagonist + ' ' + s
					protagonist = protagonist.strip()
				line = line[:line.index('<b>')+3]+protagonist+line[line.index('</b>'):]
			elif ' ' not in protagonist:
				last_guy = protagonist
				if protagonist not in stage:
					stage.add(protagonist)
			elif ' ' in protagonist:
				for p in protagonist.split(' '):
					if protagonist not in stage:
						stage.add(protagonist)


		sf.write(line)
	return nodes

def parse_edge(text, nodes, logg):
	#excep = ['ALL','All','all','BOTH','Both','both','AND','And','and','BUT','But','but', ',']
	edges = {}
	ask = False # lines ends up with ? mark
	last_guy = '' 
	last_no = 0
	spoken_to = ''
	temp = ''
	add_weight = [] # last_guy not speaked to sb. in multi times
#	all_weight = [] # more than one guy has speaked simultaneously
#	all_no = 0


	text.seek(0)
	for no, line in enumerate(text):
		if '</blockquote>' in line: # End of someone's lines
			if len(add_weight)>0:
				for char in add_weight:
					temp = last_guy +','+char
					edges[temp] = edges[temp] + no
					logg.write(str(no+1)+' -TO- Conclude weight: '+temp+', '+str(edges[temp])+'\n')
#			if len(all_weight)>0:
#				for p in all_weight:
#					for char in all_weight:
#						if char!=p:
#							# bidirection
#							temp = p +','+char
#							if temp not in edges.keys():
#								edges[temp] = no - all_no
#							else:
#								edges[temp] = edges[temp] + no - all_no
#							logg.write(str(no+1)+' -Simul- Conclude weight: '+temp+', '+str(edges[temp])+'\n')
#							
#				all_weight = []
#				all_no = 0

		elif 'SCENE' in line or 'Scene' in line:
			last_guy = ''
			last_no = 0
			ask = False
			spoken_to = ''
			add_weight = []
			logg.write(str(no+1)+' -SCENE: Clear Stage- : '+'\n')

		elif ('<a name=\"' in line or '<A NAME=' in line) and line[line.index('=')+1].isdigit()==True:#speaking lines
			#logg.write(str(no+1)+' - Speaking line: '+line)
			if '[To ' in line: # [to Sb.] 
				spoken_to = line[line.index('[To')+len('[To'):line.index(']')].strip()
				if 'but' in spoken_to:
					spoken_to = spoken_to[:spoken_to.index('but')]
				if 'except' in spoken_to:
					spoken_to = spoken_to[:spoken_to.index('except')]
				spoken_to = re.sub('and\s*','',spoken_to)
				spoken_to = re.sub(',',' ',spoken_to)

				for char in spoken_to.split(' '):
					if char in nodes and char!=last_guy:
						temp = last_guy +','+char
						add_weight.append(char)
						if temp not in edges.keys():
							edges[temp] = -no
						else:
							edges[temp] = edges[temp] - no
						logg.write(str(no+1)+' -Aside to- Start with key: '+temp+'\n')
				spoken_to  = ''

			if ask==True:# turn off the above question
				ask = False
			#print 'Last simbol of lines is :' not -2
			if '</a>' in line and line[line.index('</a>')-1]=='?'or '</A>' in line and line[line.index('</A>')-1]=='?':
				ask = True
		elif '<i>To ' in line:# To somebody
			spoken_to = line[line.index('To')+3:line.index('</i>')]
			if 'but' in spoken_to:
				spoken_to = spoken_to[:spoken_to.index('but')]
			if 'except' in spoken_to:
				spoken_to = spoken_to[:spoken_to.index('except')]
			spoken_to = re.sub('and\s*','',spoken_to)
			spoken_to = re.sub(',',' ',spoken_to)

			for char in spoken_to.split(' '):
				if char in nodes and char!=last_guy:
					temp = last_guy +','+char
					add_weight.append(char)
					if temp not in edges.keys():
						edges[temp] = -no
					else:
						edges[temp] = edges[temp] - no
					logg.write(str(no+1)+' -TO- Start with key: '+temp+'\n')
			spoken_to  = ''

		elif '<a name=\"speech' in line or '<A NAME=speech' in line: #character line
			protagonist = line[line.index('<b>')+3:line.index('</b>')]
			if 'but' in protagonist:
				protagonist = protagonist[:protagonist.index('but')]
			if 'except' in protagonist:
				protagonist = protagonist[:protagonist.index('except')]
			protagonist = re.sub('and\s*','',protagonist)
			protagonist = re.sub(',','',protagonist)
			
			logg.write(str(no+1)+' - Character line: '+protagonist+'\n')

			# Someone speak simutaneously could be seemed as silent contact before words out
#			if ' ' in protagonist: 
#				logg.write(str(no+1)+' -Simul- Spotted!: '+protagonist+'\n')
#				all_no = no
#				for p in protagonist.split(' '):
#					if p in nodes:
#						all_weight.append(p)
#				#if ask==True:
#				all_weight.remove(last_guy)
				
			
			if len(add_weight)>0: #Expell someone already counted in 'To sb.'
				for char in add_weight:
					if char in protagonist.split(' '):
						protagonist = re.sub(char,'',protagonist)
						protagonist = re.sub(r'  ','',protagonist)
						logg.write(str(no+1)+' - Exclude from TO: '+char+'\n')
				add_weight = []
			#l = set(protagonist).intersection(set(excep))
			logg.write(str(no+1)+' - After washing: '+protagonist+'\n')
			
			logg.write(str(no+1)+' - Before entering ASK: '+'\n')
			logg.write(str(no+1)+' - ask = : '+str(ask)+'\n')

			if ask==True and len(protagonist)>0: #last_guy has asked
				ask = False
				if protagonist in nodes and protagonist!=last_guy: 
					temp = last_guy +','+protagonist
					if temp not in edges.keys():
						edges[temp] = no - last_no
					else:
						edges[temp] = edges[temp] + no - last_no
					logg.write(str(no+1)+' -?1- Conclude ASK: '+temp+', '+str(edges[temp])+'\n')
				else:# Maybe confused by space in character
					for char in protagonist.split(' '):
						if char!='' and char in nodes and char!=last_guy:
							temp = last_guy +','+char
							if temp not in edges.keys():
								edges[temp] = no - last_no
							else:
								edges[temp] = edges[temp] + no - last_no
							logg.write(str(no+1)+' -?2- Conclude ASK: '+temp+', '+str(edges[temp])+'\n')
			if line[line.index('<b>')+3:line.index('</b>')] in nodes:
				last_guy = line[line.index('<b>')+3:line.index('</b>')]
				last_no = no
				logg.write(str(no+1)+' - Update last_guy: '+last_guy+'\n')
		
	return edges

def reconstruct(f,logg,chars,directed):
	isolated = []
	match = 0
	last_guy = ''
	last_no = 0
	temp = ''
	complement = {}
	flag = 0
	no = 0
	line = ''
	#to find nodes that are not connected
	for n in chars:
		match = 0
		for k in directed.keys():
			for word in re.split(r',',k):
				if n == word:
					match = 1
		if match==0:
			isolated.append(n)
	# Isolated nodes are:
	print 'Isolated node: '
	for w in isolated:
		print w+',',
	print '\n'

	logg.write('---------------Here comes compensated eges!-----------------\n')
	f.seek(0)# This is too important, or the following script would output nothing besides errors.
	#To complement
	for no,line in enumerate(f):
		if 'SCENE' in line or 'Scene' in line:
			last_guy = ''
			last_no = 0
			logg.write(str(no+1)+' -SCENE: Clear Stage- : '+'\n')
		
		elif '<a name=\"speech' in line or '<A NAME=speech' in line: #character line
			protagonist = line[line.index('<b>')+3:line.index('</b>')]
			if 'but' in protagonist:
				protagonist = protagonist[:protagonist.index('but')]
			if 'except' in protagonist:
				protagonist = protagonist[:protagonist.index('except')]
			protagonist = re.sub('and\s*','',protagonist)
			protagonist = re.sub(',','',protagonist)
			
			if protagonist!='' and last_guy!='' and protagonist in chars and protagonist!=last_guy and (protagonist in isolated or last_guy in isolated): 
				temp = last_guy +','+protagonist
				if temp not in complement.keys():
					complement[temp] = no - last_no
				else:
					complement[temp] = complement[temp] + no - last_no
				logg.write(str(no+1)+' -C1- Compensate one: '+temp+', '+str(complement[temp])+'\n')
			else:
				for char in protagonist.split(' '):
					if char!='' and last_guy!='' and char!=last_guy and (char in isolated or last_guy in isolated):
						temp = last_guy +','+char
						if temp not in complement.keys():
							complement[temp] = no - last_no
						else:
							complement[temp] = complement[temp] + no - last_no
						logg.write(str(no+1)+' -C2- Compensate one: '+temp+', '+str(complement[temp])+'\n')
			if protagonist in chars:
				last_guy = protagonist
				last_no = no
				logg.write(str(no+1)+' - Update last_guy: '+last_guy+'\n')

	print 'Done with reconstruction.'	
	return complement


def main(argv):
	#temp = ''
	tran = 0.0
	aggregate = 0.0
	mean = 0.0
	#factor = .5
	#match = False
	less = []
	ldet = 0.0
	alpha = 2
	tu =0.95
	strong_edge = 0

	f = open(argv[1],'r')
	log_file = open(argv[1][:argv[1].index('.html')]+'_log.txt','w')
	standard_file = open(argv[1][:argv[1].index('.html')]+'_standard.xml','w+')
	node_file = open(argv[1][:argv[1].index('.html')]+'_nodes.txt','w')
	edge_file = open(argv[1][:argv[1].index('.html')]+'_edges.txt','w')
#	compensated_file=open(argv[1][:argv[1].index('.html')]+'_compensated_edges.txt','w')

	node_file.write('Id,Label\n')
	
	nodes = preprocessing(f,standard_file, log_file)
	#print nodes

	edge_file.write('Source,Target,Type,Weight\n')
	edges = parse_edge(standard_file, nodes, log_file)
	
	# calculate the mean value of weights
	for k,v in edges.iteritems():
		aggregate = aggregate + v
	mean = aggregate/len(edges)
	
	print 'Mean value is '+str(mean)
	
	# count edges if it less than mean
	print 'less than mean: '
	for k,v in edges.iteritems():
	    if v<=mean:
	        less.append(v)
	        print v
	        
	print 'count of edges: '+str(len(edges))        
	print 'count of less: '+str(len(less))
	
	# count accumulative (mean-v)
	for v in less:
	    ldet+=mean-v
	    
	ldet/=len(less)
	tran = mean-alpha*ldet
	print 'ldet: '+str(ldet)
	print 'tran: '+str(tran)
	

	nodes = []
	log_file.write('-----Here comes new nodes------\n')
	# eliminate nodes without links
	for key in edges.keys():
		for k in re.split(r',',key):
			if k not in nodes:
				nodes.append(k)
				log_file.write(k+'\n')
	
	# write nodes into file
	for k,v in enumerate(nodes):
		node_file.write(str(k+1)+','+v+'\n')

	for k,v in edges.iteritems():
		##print k+','+str(v)
		for n in re.split(r',',k):
			edge_file.write(str(nodes.index(n)+1))
			edge_file.write(',')
		edge_file.write('Directed')
		edge_file.write(',')
		
		# revise into fuzzy number
		#print 'v is :'+str(v)
		if v>mean or (v<=mean and v>=tran and (v-tran)/(alpha*ldet)>tu):
			edge_file.write(str(20))
			#print 'v-t/a*l > tu:'+str((v-tran)/alpha*ldet)
			print 'Strong!'
			strong_edge+=1
		else:
			edge_file.write(str(10))
			print 'Weak!'
		edge_file.write('\n')
        print 'strong_edge count is '+str(strong_edge)
        print 'weak_edge count is '+str(len(edges)-strong_edge)

	log_file.write('---------------Here comes regular edges!--------------------\n')
	for k,v in edges.iteritems():
		log_file.write(k+','+str(v)+'\n')
	

#	print '---------------Here comes compensated edges!--------------------'
#	compensated_file.write('Source,Target,Type,Weight\n')
#	compensated = reconstruct(standard_file,log_file,nodes,edges)
#	for k,v in compensated.iteritems():
#		print k+','+str(v)
#		for n in re.split(r',',k):
#			compensated_file.write(str(nodes.index(n)+1))
#			compensated_file.write(',')
#		compensated_file.write('Directed')
#		compensated_file.write(',')
#		compensated_file.write(str(int(v*factor)))
#		compensated_file.write('\n')

#	log_file.write('---------------Here comes compensated edges!--------------------\n')
#	for k,v in compensated.iteritems():
#		log_file.write(k+','+str(v)+'\n')

if __name__ == '__main__':
    main(sys.argv)
