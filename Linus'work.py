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
#%%
#creating the graph
G=nx.Graph()
G.add_nodes_from(nodes)
for i in range(numberofnodes):
    edge_temp = dataframe['edges'][i]
    G.add_edge(i,edge_temp[1])
    G.add_edge(i,edge_temp[1])
nx.draw_circular(G, with_labels = True)

#%%
'''
Creating time evolution algorithm
time in days
'''
time=100
df.loc[df['infected'][0]]=1
infectedlist=[0]
#%%
for i in range(time):
    infectionops=df.loc[dataframe['infected'] == 1]
    #which edges get infected
    #infect=
    
#%%
'''
Using Networkx
'''
time=10
graph = gen.make_graph(10, graph_type = 'cycle', dataset = False)
#infect node 0
patient0 = {0:1}
nx.set_node_attributes(graph,patient0,'Infection')
#print(nx.get_node_attributes(graph,'Infection'))

#%%
infectedlist=[0]
for i in range(time):
    nodes=[]
    probability=[]
    for j in range(infectedlist):
        x=infectedlist[j]
        nodeforprob=(get_nodes(Graph[x])) # CHCECKL IF THESE ARE IN THE SAME ORDER
        probability=(get_edge_probability(subrgraph(Graph,x))  #produces a list
        infectionlist=(np.random.random(size=len(array_probabilities))<array_probabilities).astype(int)
        infects=np.where(infectionlist>0)
        infectedlist.append(list( nodeforprob[k] for k in infects ))
        infectedlist
        









    
    
    
