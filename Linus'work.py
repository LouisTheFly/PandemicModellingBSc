#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 13:26:14 2023

@author: Linus
"""
import networkx as nx
import matplotlib.pyplot as plt
import random 
import numpy as np
import pandas as pd
import graph_generator as gen
import copy

#%%
"""
All above were CHATGPT trials, here we are stress testing networks.
How large can we generate with the computational power we have
Try creating a graph with enough nodes to represent a population
Find largest population that can be created visually and non-visually
IN time of around 30 seconds
"""
node_names = np.arange(100)
graph = nx.DiGraph()
for i in node_names:
    graph.add_node('%s'%i)
#graph.add_edge('2','3')
nx.draw_random(graph, with_labels = True)
"""
very challenging to visualise anything over 1000

without visualisation it can run 1 million nodes with ease
a 10 million node graph takes around 1 or 2 minutes to generate
"""
#%%
"""
Functions to generate regular graphs where you can edit how many neighbours each vertex has
"""
numberofnodes=20
nodes = np.arange(numberofnodes)
Columns=('degree','edges','prob','infected')
#dictionary = dict.fromkeys(nodes)
df=pd.DataFrame(data=None,index=nodes,columns=Columns)
#%%
'''
not useful
'''
for i in range(numberofnodes):
    df['degree'][i]=2
    df['prob'][i]=[1/2,1/2]
    df['infected']=0
    if i==0:
        df['edges'][i]=[nodes[-1],i+1]
    elif i==nodes[-1]:
        df['edges'][i]=[i-1,0]
    else:
        df['edges'][i]=[i-1,i+1]
'''
not useful
Creating time evolution algorithm
time in days
'''
time=100
df.loc[df['infected'][0]]=1
infectedlist=[0]    
#%%
'''
Using Networkx
'''
time=10
graph = gen.make_graph(10, graph_type = 'cycle') # dataset = False

#infect node 0
graph = gen.infect_nodes(graph, [0])
gen.draw_graph(graph, draw_type = 'circular')
#%%
#NOW NEED TO EDIT SO IT IGNORES ALREADY INFECTED NOES
infectedlist=[0]
time=20
for i in range(time):
   #gen.draw_graph(graph, draw_type = 'circular')
   #plt.show()
   # nx.draw_circular(graph) #draw graph function will be inserted here
   print(infectedlist)
   for j in range(len(infectedlist)):
        x=infectedlist[j]
        nodes=list(nx.neighbors(graph,x))# CHCECK IF THESE ARE IN THE SAME ORDER
        nodes1=copy.deepcopy(nodes)
        nodes1.append(x)
        array_probabilities=nx.get_edge_attributes(nx.subgraph(graph,nodes1),'Probability') #produces a list of probabilities corresponding to each edge
        probs=list(array_probabilities.values())
        newinfections,graph=gen.returninfections(graph,probs,nodes)
        if len(newinfections) > 0:
            infectedlist.extend(newinfections)
            infectedlist=gen.remove_repeated(infectedlist)





    
    
    
