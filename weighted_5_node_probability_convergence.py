# statistics on convergence_weighted_5_node.txt
# output into a csv file
import re,sys, numpy as np, pandas as pd
from pandas import Series, DataFrame

def main(argv):
    author = ''
    play = ''

    sub = []
    
    play_subgraph=Series()
    l=''
    subgraph = ''
    subgraphs = []
    pro = 0.0
    pros = []
    
    f = open('./convergence_weighted_5_node.txt','r')
    fi = open('./convergence_weighted_5_node.csv','w')
    
    # first to get the full index of subgraphs
    for line in f:
        if '*:' in line or '-:' in line:
            continue
        l = re.split(':',line.strip())
        subgraph = l[0]
        if subgraph not in sub:
            sub.append(subgraph)
            
    df = DataFrame(index=sub)    
    f.seek(0)
    for line in f:
        if '*:' in line:
            author = line[10:12]
        elif '-:' in line:
            if play!='':
                play_subgraph = Series(pros,index=subgraphs)
                #play_subgraph=Series(sub_pro,index=sub,dtype=float)
                
                play_subgraph.name=author+':'+play
                play_subgraph.index.name='probability'
               
                df[play_subgraph.name]=play_subgraph
                
                #if author=='Sh':
                #    print 'play_subgraph.name = '+play_subgraph.name
                #    print play_subgraph
                #    print 'df'
                #    print df[play_subgraph.name]
            play = re.split('-',line)[6]
            subgraphs = []
            pros = []
        else:
            l = re.split(':',line.strip())
            subgraph = l[0]
            pro = float(l[-1])
            subgraphs.append(subgraph)
            pros.append(pro)
            
            #sub_pro[subgraph] = pro

    print 'sub has '+str(len(sub))+' lines.'
    #df.fillna(0)
    #print df
    df.to_csv(fi)
    #print sub
    
if __name__ == '__main__':
    main(sys.argv)
