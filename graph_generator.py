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

#Dataframe generation from graph
def make_dataframe(graph):
    index = np.arange(len(graph))
    columns=('degree','edges','prob')
    df=pd.DataFrame(data=None,index=index,columns=columns)
    #df['degree'] = nx.degree(graph)
    return df


def make_graph(nodes = 10, graph_type = 'complete'):
    
    #Choose which graph to draw
    if graph_type == 'cycle':
        G = nx.cycle_graph(nodes)
    else:
        G = nx.complete_graph(nodes)
    
    #Add node attributes
    nx.set_node_attributes(G, 0, name = 'Infection')
    
    #Add edge attributes
    nx.set_edge_attributes(G, 0.5, name = 'Probability')        
    
    return G

def draw_graph(G, draw_type = 'circular'):
    #Define shape of plot
    'nx.'+ draw_type +'_layout(G)'
    pos = nx.draw_type_layout(G)
    
    nx.draw_networkx(G, pos, with_labels = True)
    nx.draw_networkx_nodes(G, pos, node_color="tab:blue")
    #nx.draw_networkx_nodes(G, pos, nodelist=[0, 1, 2, 3], node_color="tab:red")
    nx.draw_networkx_edges(G, pos)


def infection(G, nodes_to_infect):
    nodes = dict.fromkeys(nodes_to_infect, 1)
    nx.set_node_attributes(G, nodes, name = 'Infection')
    return G

#%%
graph_test = make_graph(15, graph_type = 'cycle')
#df_test = make_dataframe(graph_test)
<<<<<<< Updated upstream



=======
>>>>>>> Stashed changes
#%%
def returninfections(array_probabilities,nodes):
        infectedlist=[]
        infectionlist=(np.random.random(size=len(array_probabilities))<array_probabilities).astype(int)
        infects=np.where(infectionlist>0)
        infectedlist.append(list( nodes[k] for k in infects ))
        return infectedlist
<<<<<<< Updated upstream

=======
    
>>>>>>> Stashed changes
