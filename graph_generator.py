# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 09:31:25 2023

@author: Louis
"""

import pandas as pd
import networkx as nx
import numpy as np
import scipy as sp

#%% Generating graphs in newtwork x

def make_graph(nodes = 10, graph_type = 'complete'):
    
    #Choose which graph to draw
    if graph_type == 'cycle':
        G = nx.cycle_graph(nodes)
    else:
        G = nx.complete_graph(nodes)
    
    #Add node attributes
    nx.set_node_attributes(G, False, name = 'Infection')
    
    #Add edge attributes
    nx.set_edge_attributes(G, 0.5, name = 'Probability')        
    
    return G

#Watts-Stroghatz(WS)

def draw_graph(G, draw_type = 'circular'):

    #Define shape of plot
    if draw_type == 'random':
        pos = nx.random_layout(G)
    else:
        pos = nx.circular_layout(G)
    
    #Find infected nodes to colour red
    infected_nodes = list({k:v for (k,v) in nx.get_node_attributes(G, 'Infection').items() if v==1})
    
    #Draw Nodes, Edges, Labels
    nx.draw_networkx_nodes(G, pos, node_color="tab:blue") #Healthy
    nx.draw_networkx_nodes(G, pos, nodelist=infected_nodes, node_color="tab:red") #Infected
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)
    return

#Dataframe generation from graph
def make_dataframe(G):
    index = np.arange(len(G))
    columns=('infection', 'degree', 'edges', 'prob')
    df=pd.DataFrame(data=None,index=index,columns=columns)
    
    #infection
    df['infection'] = dict(nx.get_node_attributes(G, 'Infection')).values()
    
    #degree
    df['degree'] = dict(nx.degree(G)).values()
    
    #subgraph
    for i in range(len(G)):
        neighbors = list(nx.neighbors(G, i))
        neighbors.append(i)
        subG = nx.subgraph(G, neighbors)
        df['edges'][i] = nx.edges(subG)
        df['prob'][i] = list(nx.get_edge_attributes(subG, 'Probability').values())
    
    return df

#Infects specified nodes
def infect_nodes(G, nodes_to_infect):
    nodes = dict.fromkeys(nodes_to_infect, True)
    nx.set_node_attributes(G, nodes, name = 'Infection')
    return G

#%%
G = make_graph(13, graph_type = 'connected')
#df_test = make_dataframe(graph_test)

G = infect_nodes(G, [10,4,8,9])

draw_graph(G, draw_type = 'circular')

df = make_dataframe(G)


#%%
def returninfections(graph,array_prob,nodes):
    infectedlist=[]
    infectionlist=(np.random.random(size=len(array_prob))<array_prob).astype(bool)
    infects=np.where(infectionlist)[0]
    
    #need to now take infect values and find corresponding node locations from nodes
    if np.any(infectionlist):
        graph=infect_nodes(graph,infects[0])
    return infectedlist,graph
