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

time_steps = 300
show = False
log = False
delay = False
plot = True
five_day_average = True

#Node Setup
nodes = 10000
graph_type = 'WS'
base_edge_prob = 0.05

#nodes_to_infect = [0]
amount_to_infect = 10
#nodes_to_vaccinate = [5,7]
amount_to_vaccinate = 0

#Infection Controls
base_infection_strength = 80 # Always make an integer, analagous to days infected
base_infection_decay = 10 # Always make an integer, analagous to days infected

#Vaccination Controls
base_vacc_strength = 0.8
base_vacc_loss = 0.01


graph = gen.make_graph(nodes = nodes, graph_type = graph_type, base_edge_prob = base_edge_prob) # dataset = False

#Infect nodes
#graph = alg.infect_nodes(graph, nodes_to_infect, base_infection_strength)
graph = alg.infect_random_nodes(graph, amount_to_infect, base_infection_strength)

#Vaccinate nodes
#graph = alg.vaccinate_nodes(graph, nodes_to_vaccinate, base_vacc_strength)
graph = alg.vaccinate_random_nodes(graph, amount_to_vaccinate, base_vacc_strength)

#Drawing
if show == True:
    gen.draw_graph(graph, draw_type = 'circular')

########Iterating########

graph, infected_list, infections_per_day, infected_nodes_count_list = alg.run_graph(graph, time_steps, show = show, log = log, delay = delay, base_infection_decay = base_infection_decay, base_vacc_loss = base_vacc_loss)

########Graphing########
if plot == True:
    alg.plotting(np.arange(time_steps),infections_per_day, 'bar', 'Infections per Day', 'Time (in days)', 'Change in Number of Infections', five_day_average = five_day_average)
    alg.plotting(np.arange(time_steps),infected_nodes_count_list, 'bar', 'Infected per Day', 'Time (in days)', 'Number of Infections', five_day_average = five_day_average)