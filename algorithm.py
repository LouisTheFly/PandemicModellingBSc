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
from time import sleep

#%%

#Main Graph Time Iterator 
def run_graph(G, time_steps = 20, show = False, log = False, delay = False):
    
    #Finds any infected nodes in the graph
    infected_nodes_list = []
    infected_nodes_list += find_infected_nodes(G)
    infected_nodes_count = len(infected_nodes_list)
    
    #Place to store count of each day's new infections
    daily_infections_list = []
    
    #Each time_step
    for i in range(time_steps):
        
        #Place to store the new nodes infected that day
        infections_within_day = []
        
        #Run through each infected node
        for j in infected_nodes_list:
            #Find adjacent to j
            neighbors = list(nx.neighbors(G,j))
            
            #Make subgraph of these
            neighbor_subG = nx.subgraph(G,neighbors)
            
            #Find the healthy ones
            healthy_neighbors = find_healthy_nodes(neighbor_subG)
            
            #Check if there are any possible nodes to infect
            if len(healthy_neighbors) == 0:
                continue
            else:
                #Make subgraph of J and its healthy neighbours
                healthy_neighbors.append(j)
                subG = nx.subgraph(G,healthy_neighbors)
                
                #Return list of new nodes to infect
                nodes_to_infect = calculate_infections(subG, j)
                
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
    nodes = dict.fromkeys(nodes_to_vaccinate, True)
    nx.set_node_attributes(G, nodes, name = 'Vaccination')
    return G

#Finds any nodes currently infected in a graph
def find_infected_nodes(G):
    nodes = list({k:v for (k,v) in nx.get_node_attributes(G, 'Infection').items() if v==True})
    return nodes

#Finds any nodes currently vaccinated in a graph
def find_vaccinated_nodes(G):
    nodes = list({k:v for (k,v) in nx.get_node_attributes(G, 'Vaccination').items() if v==True})
    return nodes

#Finds any nodes currently healthy in a graph
def find_healthy_nodes(G):
    nodes = list({k:v for (k,v) in nx.get_node_attributes(G, 'Infection').items() if v==False})
    return nodes

#For given nodes and edges, returns which have been infected
def calculate_infections(subG, centre):
    infected_nodes = []
    edge_prob = nx.get_edge_attributes(subG,'Probability')
    
    #Create lists of keys and related values
    edge_prob_keys = list(edge_prob.keys())
    edge_prob_vals = list(edge_prob.values())

    #Iterate through vals checking if they exceed the rand values, then append to list
    for i in range(len(edge_prob)):
        if np.random.random() <= edge_prob_vals[i]:
            node_found = [x for x in edge_prob_keys[i] if x != centre]
            infected_nodes.append(node_found[0])
    return infected_nodes

#%% Utility
def remove_repeated(lst):
    return list(set(lst))

def plotting(x,y,title = 'Default Title',x_label = 'Default X',y_label = 'Default Y'):
    plt.plot(x,y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid()
    plt.show()


