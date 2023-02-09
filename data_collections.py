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

graph = gen.make_graph(100, graph_type = 'WS', base_edge_prob = 0.1) # dataset = False

#Infect nodes
graph = alg.infect_nodes(graph, [0])

#Vaccinate nodes
#graph = alg.vaccinate_nodes(graph, [1,7,16,11,20,22])

#Drawing
#gen.draw_graph(graph, draw_type = 'circular')

########Iterating########

time=200
graph,infectedlist,infectionsperday=alg.run_graph(graph, time, show = False, log = False, delay = False)

########Graphing########

alg.plotting(np.arange(time),infectionsperday, 'bar', 'Infections per Day, Tot = %s'%(len(infectedlist)), 'Time (in days)', 'Number of Infections')