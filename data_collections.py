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

#other files
import graph_generator as gen
import algorithm as alg
import analysis_functions as analfunc

import cProfile
import pstats

#%% Testing

##########Setup#########

time_steps = 100
show = False
log = False
delay = False
plot = True
five_day_average = True

#Node Setup
nodes = 10000
graph_type = 'WS'
base_edge_prob = 0.1

#nodes_to_infect = [0]
amount_to_infect = 10
#nodes_to_vaccinate = [5,7]
amount_to_vaccinate = 0

#Infection Controls
base_infection_strength = 100 # Always make an integer, analagous to days infected
base_infection_decay = 10 # Always make an integer, analagous to days infected
infection_length = base_infection_strength/base_infection_decay

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

graph, infected_list, infections_per_day, infected_nodes_count_list, R_sources = alg.run_graph(graph, time_steps, show = show, log = log, delay = delay, base_infection_decay = base_infection_decay, base_vacc_loss = base_vacc_loss)

#%%
########Finding R########

##Empirical##
bins = np.linspace(0, nodes, nodes+1)
bin_means = np.histogram(R_sources, bins)[0]
bin_means_corrected = []
for i in infected_list:
    bin_means_corrected.append(bin_means[i])
empirical_R_value = round(np.mean(bin_means_corrected),3)

##Statistical##
degree_array = np.transpose(analfunc.degree_finder(graph))[1]
avg_degree = np.mean(degree_array)
statistical_R_value = round(infection_length * base_edge_prob * avg_degree, 3)

########Graphing########
if plot == True:
    alg.plotting(np.arange(time_steps),infections_per_day, 'bar', 'Infections per Day', 'Time (in days)', 'Change in Number of Infections', five_day_average = five_day_average)
    alg.plotting(np.arange(time_steps),infected_nodes_count_list, 'bar', 'Infected per Day', 'Time (in days)', 'Number of Infections', five_day_average = five_day_average)
    plt.hist(bin_means_corrected, np.linspace(0,max(bin_means_corrected), max(bin_means_corrected)+1))
    plt.title('Emp R = %s Stat R = %s'%(empirical_R_value, statistical_R_value))
    plt.show()
    
#%%   
########Optimising########
cProfile.run('alg.run_graph(graph, time_steps, show = show, log = log, delay = delay, base_infection_decay = base_infection_decay, base_vacc_loss = base_vacc_loss)', 'restats')
p = pstats.Stats('restats')
p.strip_dirs().sort_stats('cumtime').print_stats()