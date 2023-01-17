# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 19:31:14 2023

@author: Louis
"""
import networkx as nx
import numpy as np
import scipy as sp

#%%
node_names = np.arange(8)


graph = nx.DiGraph()

for i in node_names:
    graph.add_node('%s'%i)
print(graph.nodes())

graph.add_edge('2','3')

nx.draw_circular(graph, with_labels = True)
