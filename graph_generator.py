# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 09:31:25 2023

@author: Louis
"""

import pandas as pd
import networkx as nx
import numpy as np
import scipy as sp


#%%

def complete_graph(dataframe):
    nodes = list(dataframe.index)
    for i in nodes:
        temp_edges = []
        for j in nodes:
            if i != j:
                temp_edges.append(j)
        dataframe['edges'][i] = temp_edges
    return

def loop_graph(dataframe):
    nodes = list(dataframe.index)
    for i in nodes:
        temp_edges = []
        temp_edges.append((i+1)%(nodes[-1]+1))
        temp_edges.append((i-1)%(nodes[-1]+1))
        dataframe['edges'][i] = temp_edges
    return

def degree_calc(dataframe):
    for i in dataframe.index:
        dataframe['degree'][i] = len(dataframe['edges'][i])
    return
    
#########################################################


def draw_circular_graph(dataframe):
    nodes = list(dataframe.index)
    G = nx.Graph()
    G.add_nodes_from(nodes)
    for i in nodes:
        for j in dataframe['edges'][i]:
            G.add_edge(i,j)
    nx.draw_circular(G, with_labels = True)
    return

def draw_random_graph(dataframe):
    nodes = list(dataframe.index)
    G = nx.Graph()
    G.add_nodes_from(nodes)
    for i in nodes:
        for j in dataframe['edges'][i]:
            G.add_edge(i,j)
    nx.draw_random(G, with_labels = True)
    return
    

#%%
numberofnodes=12
nodes = np.arange(numberofnodes)
Columns=('degree','edges','prob')

dataframe=pd.DataFrame(data=None,index=nodes,columns=Columns)

test = dataframe

#Type of graph
complete_graph(test)
loop_graph(test)
degree_calc(test)

#Visual Graph
#draw_circular_graph(test)
draw_random_graph(test)

