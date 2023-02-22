# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 15:28:06 2023

@author: Louis
"""

import networkx as nx
import matplotlib.pyplot as plt
import random 
import numpy as np
import pandas as pd
import copy
import graph_generator as gen
import algorithm as alg

#%% Testing

##########Setup#########
time_steps = 10
show = True
log = False

nodes = 10
graph_type = 'WS'
base_edge_prob = 1
nodes_to_infect = [0]
#nodes_to_vaccinate = [5,7]
amount_to_vaccinate = 4

graph = gen.make_graph(nodes = nodes, graph_type = graph_type, base_edge_prob = base_edge_prob) # dataset = False

#Infect nodes
graph = alg.infect_nodes(graph, nodes_to_infect)

#Vaccinate nodes
#graph = alg.vaccinate_nodes(graph, nodes_to_vaccinate)
graph = alg.vaccinate_random_nodes(graph, amount_to_vaccinate)

#Drawing
gen.draw_graph(graph, draw_type = 'circular')

#%%
########Iterating########

graph,infectedlist,infectionsperday=alg.run_graph(graph, time_steps, show = show, log = log, delay = False)

########Graphing########

#alg.plotting(np.arange(time_steps),infectionsperday, 'bar', 'Infections per Day, Tot = %s'%(len(infectedlist)), 'Time (in days)', 'Number of Infections')