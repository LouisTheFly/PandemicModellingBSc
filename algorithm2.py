#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 12:07:01 2023

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
def run_graph(G, time_steps = 20, show = False, log = False, delay = False, base_vacc_loss = 0.1):
    
    #Finds any infected nodes in the graph
    positive_nodes_list = [] #Contains a list of node keys infected at any point
    positive_nodes_list += find_infected_nodes(G)
    positive_nodes_count = len(positive_nodes_list) #Number of nodes infected at any point
    
    #infective nodes
    infective_nodes_list = [] #Contains a list of node keys infected at any point
    infective_nodes_list += find_infective_nodes(G)
    infective_nodes_count = len(infective_nodes_list)
    print( infective_nodes_count )
     #Place to store count of each day's new infections
    daily_infections_list = []
    infected_nodes_count_list = []
    
    #finding days infected plus recovery period etc
    #starts with the initially infected nodes

    daysinfected=np.array([0]*len(positive_nodes_list))
    #so days infected start at 0
    #Each time_step
    for i in tqdm(range(time_steps)):
        
        daysinfected=daysinfected+1
        #Place to store the new nodes infected that day
        infections_within_day = []
        source_nodes_within_day = []
        #Run through each infective node
        for j in infective_nodes_list:
            
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
                nodes_to_infect, source_nodes = calculate_infections(G, local_subG, j)
                #check if any new nodes have been infected
                if len(nodes_to_infect) == 0:
                    continue
                else:
                    nodes_to_infect=list(filter(lambda x: x not in positive_nodes_list, nodes_to_infect))
                    print('hello',nodes_to_infect)
                    #Infect nodes and update overall list
                    infect_nodes(G, nodes_to_infect)
                    infections_within_day += nodes_to_infect
                    source_nodes_within_day += source_nodes
                    
        #Update overall infected list and remove duplicate nodes
        #infections_within_day=list(filter(lambda x: x not in infected_nodes_list,infections_within_day))
        infective_nodes_list += infections_within_day
        positive_nodes_list += infections_within_day
        #Decrement vaccination value by a certain amount, if negative set to 0
        vacc_subG = nx.subgraph(G, find_vaccinated_nodes(G)) #Make subgraph of only nodes with some ammount of vaccination
        vacc_subG_dict = nx.get_node_attributes(vacc_subG, 'Vaccination') #Get their vaccination status in a dict
        [vacc_subG_dict.update({k: max(v-base_vacc_loss, 0)}) for k, v in vacc_subG_dict.items()] #Update the value in that dict
        nx.set_node_attributes(G, vacc_subG_dict, name = 'Vaccination') #Set that new value back into G
 
        #Find how many new nodes are infected and update lists and counters
        new_inf_count = len(infections_within_day)
        infected_nodes_count = len(positive_nodes_list)
        daily_infections_list.append(new_inf_count)

    

        daysinfected=np.append(daysinfected,[0]*new_inf_count)
        print(len(daysinfected),len(positive_nodes_list),len(infective_nodes_list))
        if np.max(daysinfected)>=5:
            #this is stopping transmission
            locationinf=[]
            locationinf=np.where(np.array(daysinfected)==5)[0]
            uninfectivenodes=list(np.array(positive_nodes_list)[locationinf])
            infective_nodes_list=list(filter(lambda x: x not in uninfectivenodes, infective_nodes_list))
            stoptransmission_nodes(G,locationinf)
        if np.max(daysinfected)>=10:
            #this is healing them
            print(daysinfected==10)
            locationcure=[]
            locationcure=np.where(daysinfected==10)[0]
            daysinfected=np.delete(daysinfected,locationcure)
            positive_nodes_list
            cure_nodes(G,locationcure)
       
        #For visualising the graph
        if show == True:
            gen.draw_graph(G)
            plt.show()
            
        #For logging the graph data into the console
        if log == True:
            print('Iteration: ',i)
            print('Number of Infected Nodes...', infected_nodes_count)
            print('IDs of Infected Nodes...', positive_nodes_list)
            
        #For adding delay
        if delay == True:
            sleep(1)  
    
    #For checking validity of spread
    if log == True:
        print('Infections to date...',sum(daily_infections_list))
    
    #print(nx.get_node_attributes(G, name = 'Infected by:'))
            
    return G, infective_nodes_list, daily_infections_list



#Infects specified nodes
def infect_nodes(G, nodes_to_infect):
    nodes = dict.fromkeys(nodes_to_infect, True)
    nx.set_node_attributes(G, nodes, name = 'Infection')
    nx.set_node_attributes(G, nodes, name = 'Infective')    
    return G

def infect_random_nodes(G, amount_to_infect):
    healthy_nodes = find_healthy_nodes(G)
    nodes_to_infect = np.random.choice(healthy_nodes, size = amount_to_infect, replace = False)
    nodes = dict.fromkeys(nodes_to_infect, True)
    nx.set_node_attributes(G, nodes, name = 'Infection')
    nx.set_node_attributes(G, nodes, name = 'Infective')
    return G

'''
iadd another function adding a vaccination stance as well, i.e infective for 5 days but still 
'''
#Cures specified nodes
def cure_nodes(G, nodes_to_cure):
    nodes = dict.fromkeys(nodes_to_cure, False)
    nx.set_node_attributes(G, nodes, name = 'Infection')    
    return G

def stoptransmission_nodes(G, nodes_to_cure):
    nodes = dict.fromkeys(nodes_to_cure, False)
    nx.set_node_attributes(G, nodes, name = 'Infective')    
    return G

#Vaccinate specified nodes
def vaccinate_nodes(G, nodes_to_vaccinate, base_vacc_strength = 0.7):
    nodes = dict.fromkeys(nodes_to_vaccinate, base_vacc_strength)
    nx.set_node_attributes(G, nodes, name = 'Vaccination')
    return G

def vaccinate_random_nodes(G, amount_to_vaccinate, base_vacc_strength = 0.7):
    healthy_nodes = find_healthy_nodes(G)
    nodes_to_vaccinate = np.random.choice(healthy_nodes, size = amount_to_vaccinate, replace = False)
    nodes = dict.fromkeys(nodes_to_vaccinate, base_vacc_strength)
    nx.set_node_attributes(G, nodes, name = 'Vaccination')
    return G

#Finds any nodes currently infected in a graph
def find_infected_nodes(G):
    nodes = list({k:v for (k,v) in nx.get_node_attributes(G, 'Infection').items() if v==True})
    return nodes
#finds infective nodes
def find_infective_nodes(G):
    nodes = list({k:v for (k,v) in nx.get_node_attributes(G, 'Infective').items() if v==True})
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
def calculate_infections(G, subG, centre):
    #Create empty bin for nodes that get infected
    infected_nodes = []
    source_nodes = []
    
    #Create and order dictionaries of edges and vaccination status
    edge_prob = nx.get_edge_attributes(subG, 'Probability')
    edge_prob = OrderedDict(sorted(edge_prob.items()))
    
    #Create lists of keys and related values
    edge_prob_keys = list(edge_prob.keys())
    edge_prob_vals = list(edge_prob.values())

    #Iterate through vals checking if they exceed the rand values, then append to list
    for i in range(len(edge_prob)):
        if np.random.random() <= edge_prob_vals[i]:
            node_found = [x for x in edge_prob_keys[i] if x != centre][0]
            infected_nodes.append(node_found)
            source_nodes.append(centre)

    return infected_nodes, source_nodes

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


