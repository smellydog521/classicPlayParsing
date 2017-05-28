# calculate the probabilities of every weighted subgraph of 4 nodes
# put <edge_count, bi_edge_count> as sugraph id

import re,sys,os

def main(argv):
  key = ''
	rf = ''
	f = ''
	con_file = ''
	line = ''
	
	# strong and weak count
	sedge = wedge = 0
	
	# strong and weak probability
	spro = wpro = 0.0
	
	# set up a map for spro and wpro
	spwp = {}
	
	# subgraph counts, 
	subgraph = {}
	temp = []
	
	# integrate all data into one file
	convergence_file = open('convergence_weighted_4_node.txt','a')
	convergence_file.write('**********'+argv[1]+'**********:\n')

	for parents,dirnames,filenames in os.walk(argv[1]):
		for fn in filenames:
			if '_edges.txt' in fn:
			        print '------Begin Watching '+fn+'--------'
			        sedge = wedge = 0; spro = wpro = 0.0
			    	ef = open(argv[1]+'/'+fn,'r')
			    	for line in ef:
			    		if('Source' in line):
						continue
					if ('Directed,20' in line):
						sedge+=1
					if ('Directed,10' in line):
						wedge+=1
				spro=float(sedge)/(sedge+wedge);
				wpro=float(wedge)/(sedge+wedge);
				
				k1 = fn[:fn.index('_')]
				spwp[k1]=str(spro)+','+str(wpro)
				
			        print 'spro '+str(spro)
			        print 'wpro '+str(wpro)
	
	# to get subgraph in enumeration
				
	# to compute the probability		        
	for parents,dirnames,filenames in os.walk(argv[1]):		
		for fn in filenames:
			if 'weighted_4_node_subgraph.txt' in fn and 'edges' not in fn:
				print '------Begin Processing '+fn+'--------'
				convergence_file.write('------'+fn[:fn.index('_')]+'------:\n')
				
				key = ''
				line = ''
				subgraph = {}
				
				k2 = fn[:fn.index('_')]
				spro = float(re.split(',',spwp[k2])[0])
				wpro = float(re.split(',',spwp[k2])[1])
				
				#print 'Current '+k2
				#print 'spro '+str(spro)
				#print 'wpro '+str(wpro)

				rf = open(argv[1]+'/'+fn,'r')
				f = open(argv[1]+'/'+fn[:fn.index('_')]+'_weighted_4_node_subgraph_original.txt','w+')
				con_file = open(argv[1]+'/'+fn[:str(fn).index('_')]+'_weighted_4_node_subgraph_convergence.txt','w+')
				
				flag = False
				
				for line in rf:
					if('Subgraph' in line and not flag):
					        flag = True
						continue
					elif('Subgraph' in line and flag):
					        flag = False
						break
					else:
					        f.write(line)
				
				#f.seek(0)
				#for line in f:
				#    temp = re.split(',',re.split(':',line.strip())[0])
				#    occur = int(re.split(',',re.split(':',line.strip())[1])[-1])
				#    key = temp[0] + ',' + temp[1]
				#    if key not in subgraph.keys():
				#        subgraph[key]=occur
				#    else: 
				#        subgraph[key]+=occur
				        
				#print 'subgraph are: '
				#for k,v in subgraph.iteritems():
				#    print k+':'+str(v)
					
				f.seek(0)
				for line in f:
				        #print line
					cat = re.split(':',line.strip())
					
					ebsw = re.split(',',cat[0])
					weighted_count = re.split(',',cat[1])
					binary_count = re.split(',',cat[2])
					
					sc = int(ebsw[2])
					wc = int(ebsw[3])
					#key = swcount[-1]
					em = int(weighted_count[1])
					ebm = int(binary_count[1])
					#occur = int(odoccur[1]) # tune this into odoccur[0] for total occurence
					
					temp = pow(spro,sc)*pow(wpro,wc)
						
					pro = pow(temp,em)*pow(1-temp,ebm-em)
					
					#if scount==0 and wcount==2 and key=='1':
					#        print 'scount' + str(scount)
					#        print 'wcount' + str(wcount)
					#	print 'temp = '+str(temp)
					
					con_file.write(line.strip()+':'+str(pro)+'\n')
					convergence_file.write(line.strip()+':'+str(pro)+'\n')				
				
				print '======End Processing '+fn+'======'
	# leveraging probability convergence, to trigger last play's computation			
	convergence_file.write('------------:\n')
	convergence_file.close()
if __name__ == '__main__':
    main(sys.argv)
