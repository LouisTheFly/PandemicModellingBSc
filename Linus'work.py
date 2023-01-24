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
Columns=('degree','edges','prob')
#dictionary = dict.fromkeys(nodes)
dataframe=pd.DataFrame(data=None,index=nodes,columns=Columns)
#%%
for i in range(numberofnodes):
    dataframe['degree'][i]=2
    dataframe['prob'][i]=1/2
    if i==0:
        dataframe['edges'][i]=[nodes[-1],i+1]
    elif i==nodes[-1]:
        dataframe['edges'][i]=[i-1,0]
    else:
        dataframe['edges'][i]=[i-1,i+1]
#%%
#creating the graph
G=nx.Graph()
G.add_nodes_from(nodes)
for i in range(numberofnodes):
    edge_temp = dataframe['edges'][i]
    G.add_edge(i,edge_temp[1])
    G.add_edge(i,edge_temp[1])
nx.draw_circular(G, with_labels = True)

    
    
    
    
    
    
    
    
