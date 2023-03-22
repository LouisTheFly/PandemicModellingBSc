#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 23:19:35 2023

@author: Linus
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


time_steps = 15
show = True
log = False
delay = False
plot = False

###### Node Setup - Change These ############
nodes = 10
graph_type = 'cycle'

#These get multiplied to form the base_edge_prob
meeting_chance = 1
transmission_chance = 1


###### Scenario Controls - Change These #############
#Infection Controls
infectivity_period = 5 #Days in which it can infect other nodes
immunity_period = 5 #Days after infectivity period ends
infection_dose = 10 #%

#Vaccination Controls
rate_vaccination_loss = 100 #% #Common to natural and forced immunity

vaccination_effectiveness = 0 #% #Just for forced vaccination
vaccination_dose = 0 #%

###### Derived Quantities - DO NOT CHANGE ###############
base_infection_decay = 1 
base_infection_strength = base_infection_decay * infectivity_period 
base_edge_prob = meeting_chance * transmission_chance

base_vacc_strength = vaccination_effectiveness/100
base_vacc_loss = rate_vaccination_loss/100
infection_immunity_strength = 5

#nodes_to_infect = [0]
amount_to_infect = int(round(infection_dose/100*nodes))
if amount_to_infect < 1:
    raise ValueError('No nodes will be infected - raise dosage')
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
#if show == True:
 #   gen.draw_graph(graph, draw_type = 'cycle')
    


########Iterating########

graph, infected_nodes_list, gross_infections_per_day, net_infections_per_day, ever_infections_list, infected_nodes_count_list, R_cum_vals_list = alg.run_graph(graph, time_steps, show = show, log = log, delay = delay, base_infection_strength = base_infection_strength, base_infection_decay = base_infection_decay, base_vacc_loss = base_vacc_loss)


########Finding R########
##Empirical##

#Remove 'nans' from infectivity period
R_cum_vals_list = R_cum_vals_list[infectivity_period:]

#5 Day average count, exludes nans but keeps zeroes
R_emp_vals_list = [float('nan'), float('nan')]
R_emp_std_list = [float('nan'), float('nan')]

for i in range(2, len(R_cum_vals_list)-2):
    R_temp_list = []
    R_temp_list += R_cum_vals_list[i-2]
    R_temp_list += R_cum_vals_list[i-1]
    R_temp_list += R_cum_vals_list[i]
    R_temp_list += R_cum_vals_list[i+1]
    R_temp_list += R_cum_vals_list[i+2]
    R_emp_vals_list.append(np.mean(R_temp_list))
    R_emp_std_list.append(np.std(R_temp_list))


#Add nans to make list correct length
for i in range(infectivity_period+2):
    R_emp_vals_list.append(float('nan'))
    R_emp_std_list.append(float('nan'))
    

##Statistical##
degree_array = np.transpose(analfunc.degree_finder(graph))[1]
avg_degree = np.mean(degree_array)
R0 = round((1-(1-base_edge_prob)**infectivity_period) * avg_degree, 3)
R_stat_vals_list = []
for i in range(time_steps):
    R_stat_vals_list.append(R0 * (nodes - infected_nodes_count_list[i]) / nodes)

#%%
########Graphing########
if plot == True:
    #X axis
    xaxis = np.arange(time_steps)

    alg.plotting(xaxis,net_infections_per_day, 'bar', 'Net Infections per Day', 'Time (in days)', 'Change in Number of Infections', five_day_average = True)
    alg.plotting(xaxis,gross_infections_per_day, 'bar', 'Gross Infections per Day', 'Time (in days)', 'Change in Number of Infections', five_day_average = True)
    alg.plotting(xaxis,infected_nodes_count_list, 'bar', 'Infected per Day', 'Time (in days)', 'Number of Infections', five_day_average = True)

    
    plt.plot(xaxis, R_emp_vals_list, 'x')
    plt.plot(xaxis, alg.moving_average(R_emp_vals_list, 4), 'x')
    plt.plot(xaxis, R_stat_vals_list)
    plt.show()

  
########Optimising########
#cProfile.run('alg.run_graph(graph, time_steps, show = show, log = log, delay = delay, base_infection_decay = base_infection_decay, base_vacc_loss = base_vacc_loss)', 'restats')
#p = pstats.Stats('restats')
#p.strip_dirs().sort_stats('cumtime').print_stats()



#%%
'''
Basic model

run for 1 year
no vacc
no recovery
cycle
50% meeting chance and 50% transmission
infective forever
no recovery
infect 1

'''
#initialisation
time_steps = 365
show = False
log = False
delay = False
plot = True

###### Node Setup - Change These ############
nodes = 100000
graph_type = 'cycle'

#These get multiplied to form the base_edge_prob
meeting_chance = 0.5
transmission_chance = 0.5


###### Scenario Controls - Change These #############
#Infection Controls
infectivity_period = 365 #Days in which it can infect other nodes
immunity_period = 0 #Days after infectivity period ends
infection_dose = 0 #%

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
#amount_to_infect = int(round(infection_dose/100*nodes))
amount_to_infect = 1
if amount_to_infect < 1:
    raise ValueError('No nodes will be infected - raise dosage')
#nodes_to_vaccinate = [5,7]
amount_to_vaccinate = 0#int(round(vaccination_dose/100*nodes))

graphtot=np.full(10,0)
infected_nodes_listtot=np.full(10,0)
gross_infections_per_daytot=np.full(10,0)
net_infections_per_daytot=np.full(10,0)
ever_infections_listtot=np.full(10,0)
infected_nodes_count_listtot=np.full(10,0)
R_cum_vals_listtot=np.full(10,0)
#run algorithm, get results
for i in range(10):
    graphtot[i], infected_nodes_listtot[i], gross_infections_per_daytot[i], net_infections_per_daytot[i], ever_infections_listtot[i], infected_nodes_count_listtot[i], R_cum_vals_listtot[i] = alg.run_graph(graph, time_steps, show = show, log = log, delay = delay, base_infection_strength = base_infection_strength, base_infection_decay = base_infection_decay, base_vacc_loss = base_vacc_loss)




#%%
'''
Functions to call upon
'''

def meanlists(a):
    meanlist=np.mean(a,axis=0)
    return meanlist
def stdlist(a):
    stdlist=np.std(a,axis=0)
    return stdlist




#%%

list1=['a','b','c','d','e','f','g','h','i','j']










