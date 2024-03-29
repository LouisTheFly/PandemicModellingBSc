#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 13:05:57 2023

@author: Linus
"""


import networkx as nx
import matplotlib.pyplot as plt
import random 
import numpy as np
import pandas as pd
import copy
import graph_generator as gen
import linus_graph_generator as lin
import algorithm2 as alg

#%% Testing

##########Setup#########


time_steps = 100

show = False
log = False
delay = False
plot = False
five_day_average = True

nodes = 1000
graph_type = 'WS'
base_edge_prob = 0.5
#nodes_to_infect = [0]
amount_to_infect = 10
#nodes_to_vaccinate = [5,7]
amount_to_vaccinate = 0
#Node Setup
#nodes = 10
#graph_type = 'WS'
#base_edge_prob = 0.05

#Vaccination Controls
base_vacc_strength = 1
base_vacc_loss = 0


graph = lin.make_graph(nodes = nodes, graph_type = graph_type, base_edge_prob = base_edge_prob) # dataset = False

#Infect nodes
# = alg.infect_nodes(graph, nodes_to_infect)
graph = alg.infect_random_nodes(graph, amount_to_infect)

#Vaccinate nodes
#graph = alg.vaccinate_nodes(graph, nodes_to_vaccinate)
graph = alg.vaccinate_random_nodes(graph, amount_to_vaccinate, base_vacc_strength)

#Drawing
if show == True:
    gen.draw_graph(graph, draw_type = 'circular')

########Iterating########

graph,infectedlist,infectionsperday=alg.run_graph(graph, time_steps, show = show, log = log, delay = delay, base_vacc_loss = base_vacc_loss)

########Graphing########
if plot == True:
    alg.plotting(np.arange(time_steps),infectionsperday, 'bar', 'Infections per Day', 'Time (in days)', 'Number of Infections', five_day_average = five_day_average)
    
    
    
    
    
    
    
    
    
    
    
    