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

###### Setup - Change These ############

time_steps = 400
show = False
log = False
delay = False
plot = True

###### Node Setup - Change These ############
nodes = 10000
graph_type = 'WS'

#These get multiplied to form the base_edge_prob
meeting_chance = 0.2
transmission_chance = 0.3


###### Scenario Controls - Change These #############
#Infection Controls
infectivity_period = 10 #Days in which it can infect other nodes
immunity_period = 20 #Days after infectivity period ends
infection_dose = 1 #%

#Vaccination Controls
rate_vaccination_loss = 1 #% #Common to natural and forced immunity

vaccination_effectiveness = 80 #% #Just for forced vaccination
vaccination_dose = 0 #%

###### Derived Quantities - DO NOT CHANGE ###############
base_infection_decay = 1 
base_infection_strength = base_infection_decay * infectivity_period 
base_edge_prob = meeting_chance * transmission_chance

base_vacc_strength = vaccination_effectiveness/100
base_vacc_loss = rate_vaccination_loss/100
infection_immunity_strength = 1 + immunity_period * rate_vaccination_loss

#nodes_to_infect = [0]
amount_to_infect = int(round(infection_dose/100*nodes))
#nodes_to_vaccinate = [5,7]
amount_to_vaccinate = int(round(vaccination_dose/100*nodes))

#############################################################

graph = gen.make_graph(nodes = nodes, graph_type = graph_type, base_edge_prob = base_edge_prob) # dataset = False

#Infect nodes
#graph = alg.infect_nodes(graph, nodes_to_infect, base_infection_strength, infection_immunity_strength)
graph = alg.infect_random_nodes(graph, amount_to_infect, base_infection_strength, infection_immunity_strength)

#Vaccinate nodes
#graph = alg.vaccinate_nodes(graph, nodes_to_vaccinate, base_vacc_strength)
graph = alg.vaccinate_random_nodes(graph, amount_to_vaccinate, base_vacc_strength)

#Drawing
if show == True:
    gen.draw_graph(graph, draw_type = 'circular')


########Iterating########

graph, infected_list, gross_infections_per_day, net_infections_per_day, infected_nodes_count_list, R_sources = alg.run_graph(graph, time_steps, show = show, log = log, delay = delay, base_infection_strength = base_infection_strength, base_infection_decay = base_infection_decay, base_vacc_loss = base_vacc_loss)


########Finding R########
if plot == True:
##Empirical##
    bins = np.linspace(0, nodes, nodes+1)
    bin_means = np.histogram(R_sources, bins)[0]
    if len(infected_list) != 0:
        bin_means_corrected = []
        for i in infected_list:
            bin_means_corrected.append(bin_means[i])
        empirical_R_value = round(np.mean(bin_means_corrected),3)
    
    ##Statistical##
    degree_array = np.transpose(analfunc.degree_finder(graph))[1]
    avg_degree = np.mean(degree_array)
    statistical_R_value = round(infectivity_period * base_edge_prob * avg_degree, 3)

########Graphing########
    alg.plotting(np.arange(time_steps),net_infections_per_day, 'bar', 'Net Infections per Day', 'Time (in days)', 'Change in Number of Infections', five_day_average = True)
    alg.plotting(np.arange(time_steps),gross_infections_per_day, 'bar', 'Gross Infections per Day', 'Time (in days)', 'Change in Number of Infections', five_day_average = True)
    alg.plotting(np.arange(time_steps),infected_nodes_count_list, 'bar', 'Infected per Day', 'Time (in days)', 'Number of Infections', five_day_average = True)
    if len(infected_list) != 0:
        plt.hist(bin_means_corrected, np.linspace(0,max(bin_means_corrected), max(bin_means_corrected)+1), width = 0.9)
        plt.title('Emp R = %s Stat R = %s'%(empirical_R_value, statistical_R_value))
    plt.show()
    
  
########Optimising########
#cProfile.run('alg.run_graph(graph, time_steps, show = show, log = log, delay = delay, base_infection_decay = base_infection_decay, base_vacc_loss = base_vacc_loss)', 'restats')
#p = pstats.Stats('restats')
#p.strip_dirs().sort_stats('cumtime').print_stats()