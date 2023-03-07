#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 11:39:14 2023

@author: Linus
"""
import pandas as pd
import networkx as nx
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import graph_generator as gen
import sys
from time import sleep
from collections import OrderedDict
from tqdm import tqdm
#%%

#Main Graph Time Iterator 
def run_graph(G, time_steps = 20, show = False, log = False, delay = False):
    
    #Finds any infected nodes in the graph
    infected_nodes_list = []
    infected_nodes_list += find_infected_nodes(G)
    infected_nodes_count = len(infected_nodes_list)
    
    
    #Place to store count of each day's new infections
    daily_infections_list = []
    
    #Calculate total node count
    totalnodes=len(G)
    
    #Each time_step
    for i in tqdm(range(time_steps)):
        
        #Place to store the new nodes infected that day
        infections_within_day = []
        
        #Run through each infected node
        for j in infected_nodes_list:
            #Find adjacent to j
            edges_adj = nx.edges(G,j)
            
            #Make subgraph of these
            local_subG = G.edge_subgraph(edges_adj)
            
            #Find the healthy ones
            healthy_neighbors = find_healthy_nodes(local_subG)
            
            #Check if there are any possible nodes to infect
            if len(healthy_neighbors) == 0:
                continue
            else:
                #Return list of new nodes to infect
                nodes_to_infect = calculate_infections(local_subG, j)
                
                #Check if any new nodes have actually been infected
                if len(nodes_to_infect) == 0:
                    continue
                else:
                    #Infect nodes and update overall list
                    infect_nodes(G, nodes_to_infect)
                    infections_within_day += nodes_to_infect
                    
        #Update overall infected list and remove duplicate nodes
        infected_nodes_list += infections_within_day
        infected_nodes_list = [*set(infected_nodes_list)]
        
        #Find how many new nodes are infected and update lists and counters
        new_inf_count = len(infected_nodes_list) - infected_nodes_count
        infected_nodes_count = len(infected_nodes_list)
        daily_infections_list.append(new_inf_count)
      
        
        #if infected_nodes_count >= len(G)-3:
            #print('Nodes to be infected: ',nodes_to_infect)
            #sys.exit('Vaccinated node was infected')
        
      
        #For visualising the graph
        if show == True:
            gen.draw_graph(G)
            plt.show()
            
        #For logging the graph data into the console
        if log == True:
            print('Iteration: ',i)
            print('Number of Infected Nodes...', infected_nodes_count)
            print('IDs of Infected Nodes...', infected_nodes_list)
            
        #For adding delay
        if delay == True:
            sleep(1)          
            
        
    #For checking validity of spread
    if log == True:
        print('Infections to date...',sum(daily_infections_list))
            
    return G, infected_nodes_list, daily_infections_list


#Infects specified nodes
def infect_nodes(G, nodes_to_infect):
    nodes = dict.fromkeys(nodes_to_infect, True)
    nx.set_node_attributes(G, nodes, name = 'Infection')    
    return G

#Vaccinate specified nodes
def vaccinate_nodes(G, nodes_to_vaccinate):
    nodes = dict.fromkeys(nodes_to_vaccinate, 0.7)
    nx.set_node_attributes(G, nodes, name = 'Vaccination')
    return G

def vaccinate_random_nodes(G, amount_to_vaccinate):
    healthy_nodes = find_healthy_nodes(G)
    nodes_to_vaccinate = np.random.choice(healthy_nodes, size = amount_to_vaccinate, replace = False)
    nodes = dict.fromkeys(nodes_to_vaccinate, 0.7)
    nx.set_node_attributes(G, nodes, name = 'Vaccination')
    return G

#Finds any nodes currently infected in a graph
def find_infected_nodes(G):
    nodes = list({k:v for (k,v) in nx.get_node_attributes(G, 'Infection').items() if v==True})
    return nodes

#Finds any nodes currently vaccinated in a graph
def find_vaccinated_nodes(G):
    nodes = list({k:v for (k,v) in nx.get_node_attributes(G, 'Vaccination').items() if v!=0})
    return nodes

#Finds any nodes currently healthy in a graph
def find_healthy_nodes(G):
    nodes = list({k:v for (k,v) in nx.get_node_attributes(G, 'Infection').items() if v==False})
    return nodes

#For given nodes and edges, returns which have been infected
def calculate_infections(subG, centre):
    #Create empty bin for nodes that get infected
    infected_nodes = []
    
    #Create and order dictionaries of edges and vaccination status
    edge_prob = nx.get_edge_attributes(subG, 'Probability')
    edge_prob = OrderedDict(sorted(edge_prob.items()))

    vacc_status = nx.get_node_attributes(subG, 'Vaccination')
    vacc_status = OrderedDict(sorted(vacc_status.items()))
    
    #Create lists of keys and related values
    edge_prob_keys = list(edge_prob.keys())
    edge_prob_vals = list(edge_prob.values())
    vacc_status_keys = list(vacc_status.keys())
    vacc_status_vals = list(vacc_status.values())

    #Find the central node in the vaccination status and remove
    vacc_centre_index = [i for i, value in enumerate(vacc_status_keys) if value == centre][0]
    del vacc_status_keys[vacc_centre_index]
    del vacc_status_vals[vacc_centre_index]

    #Iterate through vals checking if they exceed the rand values, then append to list
    for i in range(len(edge_prob)):
        if np.random.random() <= edge_prob_vals[i]:
            node_found = [x for x in edge_prob_keys[i] if x != centre][0]

            #Check vaccination doesnt prevent infection
            vacc_status_index = [i for i, value in enumerate(vacc_status_keys) if value == node_found][0]
            if np.random.random() >= vacc_status_vals[vacc_status_index]:
                infected_nodes.append(node_found)
               
    return infected_nodes

#%% Utility
def remove_repeated(lst):
    return list(set(lst))

def plotting(x,y, g_type = 'line', title = 'Default Title',x_label = 'Default X',y_label = 'Default Y', five_day_average = False):
    
    #Line or bar chart
    if g_type == 'bar':
        plt.bar(x,y, width = 1)
    else:
        plt.plot(x,y)
    
    #Adds a 5 day moving average line
    if five_day_average == True:
        z = np.empty(len(x))
        for i in range(2,len(x)-2):
            z[i] = (y[i-2]+y[i-1]+y[i]+y[i+1]+y[i+2])/5
        plt.plot(x[2:-2],z[2:-2], c='red')
    
    #Visual stuff
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid()
    plt.show()


