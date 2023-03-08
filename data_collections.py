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

time_steps = 80
show = True
log = False
plot = True
five_day_average = True

nodes = 20
graph_type = 'cycle'
base_edge_prob = 1
#nodes_to_infect = [0]
amount_to_infect = 1
#nodes_to_vaccinate = [5,7]
amount_to_vaccinate = 0


graph = gen.make_graph(nodes = nodes, graph_type = graph_type, base_edge_prob = base_edge_prob) # dataset = False

#Infect nodes
#graph = alg.infect_nodes(graph, nodes_to_infect)
graph = alg.infect_random_nodes(graph, amount_to_infect)

#Vaccinate nodes
#graph = alg.vaccinate_nodes(graph, nodes_to_vaccinate)
graph = alg.vaccinate_random_nodes(graph, amount_to_vaccinate)

#Drawing
if show == True:
    gen.draw_graph(graph, draw_type = 'circular')

########Iterating########

graph,infectedlist,infectionsperday=alg.run_graph(graph, time_steps, show = show, log = log, delay = False)

########Graphing########
if plot == True:
    alg.plotting(np.arange(time_steps),infectionsperday, 'bar', 'Infections per Day', 'Time (in days)', 'Number of Infections', five_day_average = five_day_average)