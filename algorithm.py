#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 11:39:14 2023

@author: Linus
"""
import time
import pandas as pd
import networkx as nx
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import graph_generator as gen
import sys
import copy
from time import sleep
from collections import OrderedDict
from tqdm import tqdm
#%%

#Main Graph Time Iterator 
def run_graph(G, time_steps = 20, show = False, log = False, delay = False, base_infection_strength = 5, base_infection_decay = 1, base_vacc_loss = 0.1):
    
    #Finds any infected nodes in the graph
    infected_nodes_list = [] #Contains a list of node keys infected at any point
    infected_nodes_list += find_infected_nodes(G) #Easier to read but not neccesary as 2 lines
    infected_nodes_count = len(infected_nodes_list) #Number of nodes infected at any point
    prev_infected_nodes_list = infected_nodes_list
    
    #Place to store count of each day's new infections
    net_infections_list = []
    gross_infections_list = []
    ever_infections_list = []
    infected_nodes_count_list = []
    
    #For R calc
    R_cum_vals_list = []
    rolling_source_list = []
    
    #Each time_step
    for i in tqdm(range(time_steps)):
        
        #For logging the graph data into the console
        if log == True:
            print('Iteration: ',i)
            print('Number of Infected Nodes...', infected_nodes_count)
            #print('IDs of Infected Nodes...', infected_nodes_list)
        
        #Place to store the new nodes infected that day
        infections_within_day = []
        source_nodes_within_day = []
        infected_nodes_list = find_infected_nodes(G)
        
        #For R calculation
        cured_nodes_list = list(filter(lambda x: x not in infected_nodes_list, prev_infected_nodes_list))
        R_day = []
        for i in cured_nodes_list:
            R_day.append(rolling_source_list.count(i))

        R_cum_vals_list.append(R_day)
        
        #Deleting calculated R valls from roling source list
        rolling_source_list = list(filter(lambda x: x not in cured_nodes_list, rolling_source_list))
        
        #Decrement vaccination value by a certain amount, if negative set to 0
        vacc_subG = nx.subgraph(G, find_vaccinated_nodes(G)) #Make subgraph of only nodes with some ammount of vaccination
        if nx.number_of_nodes(vacc_subG) > 0:
            vacc_subG_dict = nx.get_node_attributes(vacc_subG, 'Vaccination') #Get their vaccination status in a dict
            [vacc_subG_dict.update({k: max(v-base_vacc_loss, 0)}) for k, v in vacc_subG_dict.items()] #Update the value in that dict
            nx.set_node_attributes(G, vacc_subG_dict, name = 'Vaccination') #Set that new value back into G
        
        #Decrement infection value by a certain amount, if negative set to 0
        inf_subG = nx.subgraph(G, infected_nodes_list) #Make subgraph of only nodes with some ammount of infection
        if nx.number_of_nodes(inf_subG) > 0:
            inf_subG_dict = nx.get_node_attributes(inf_subG, 'Infection') #Get their infection status in a dict
            [inf_subG_dict.update({k: max(v-base_infection_decay, 0)}) for k, v in inf_subG_dict.items()] #Update the value in that dict
            nx.set_node_attributes(G, inf_subG_dict, name = 'Infection') #Set that new value back into G

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
                nodes_to_infect, source_nodes = calculate_infections(G, local_subG, j)
                
                #Check if any new nodes have actually been infected
                if len(nodes_to_infect) == 0:
                    continue
                else:
                    infections_within_day += nodes_to_infect
                    source_nodes_within_day += source_nodes

        
        #Take collated possible infections and check vaccination doesnt prevent infection
        if len(infections_within_day) != 0:
            confirmed_infections = []
            confirmed_sources = []
            infections_subG = G.subgraph(infections_within_day)
            
            #Find vaccination status
            vacc_status = nx.get_node_attributes(infections_subG, 'Vaccination')
            vacc_status = OrderedDict(sorted(vacc_status.items()))
            vacc_status_keys = np.array(list(vacc_status.keys()))
            vacc_status_vals = np.array(list(vacc_status.values()))

            #Run probability
            for i in range(len(infections_within_day)):
                vacc_val = vacc_status_vals[np.where(vacc_status_keys == infections_within_day[i])]
                if np.random.random() >= vacc_val:
                    confirmed_infections.append(infections_within_day[i])
                    confirmed_sources.append(source_nodes_within_day[i])
            infections_within_day = confirmed_infections       
            rolling_source_list += confirmed_sources
        
        if len(infections_within_day) != 0:
            #Infect (Vaccinate) nodes and update overall list
            infect_nodes(G, infections_within_day, base_infection_strength)
            
            #Label source of infection attribute
            source_labels_dict = dict(zip(confirmed_infections, confirmed_sources))
            nx.set_node_attributes(G, source_labels_dict, name = 'Infected by:')   
            
        #Update overall infected list and remove duplicate nodes
        infected_nodes_list += infections_within_day
        infected_nodes_list = [*set(infected_nodes_list)]
        prev_infected_nodes_list = copy.deepcopy(infected_nodes_list)
        
        #Update ever infected list and remove duplicate nodes
        ever_infections_list += infections_within_day
        ever_infections_list = [*set(ever_infections_list)]
        
        #Find how many new nodes are infected and update lists and counters
        new_infected_nodes_count = len(infected_nodes_list)
        inf_count_difference = new_infected_nodes_count - infected_nodes_count
        net_infections_list.append(inf_count_difference)
        gross_infections_list.append(len(infections_within_day))
        infected_nodes_count_list.append(new_infected_nodes_count)
                
        #Update count
        infected_nodes_count = new_infected_nodes_count
        
        #For visualising the graph
        if show == True:
            gen.draw_graph(G)
            plt.show()
            
            
        #For adding delay
        if delay == True:
            sleep(1)  
 
            
    return G, infected_nodes_list, gross_infections_list, net_infections_list, ever_infections_list, infected_nodes_count_list, R_cum_vals_list


#Infects specified nodes
def infect_nodes(G, nodes_to_infect, base_infection_strength = 5, infection_immunity_strength = 1.1):
    nodes = dict.fromkeys(nodes_to_infect, base_infection_strength)
    nx.set_node_attributes(G, nodes, name = 'Infection')
    nodes = dict.fromkeys(nodes_to_infect, infection_immunity_strength)
    nx.set_node_attributes(G, nodes, name = 'Vaccination')    
    return G

def infect_random_nodes(G, amount_to_infect, base_infection_strength = 5, infection_immunity_strength = 1.1):
    healthy_nodes = find_healthy_nodes(G)
    nodes_to_infect = np.random.choice(healthy_nodes, size = amount_to_infect, replace = False)
    nodes = dict.fromkeys(nodes_to_infect, base_infection_strength)
    nx.set_node_attributes(G, nodes, name = 'Infection')
    nodes = dict.fromkeys(nodes_to_infect, infection_immunity_strength)
    nx.set_node_attributes(G, nodes, name = 'Vaccination') 
    return G

#Cures specified nodes
def cure_nodes(G, nodes_to_cure):
    nodes = dict.fromkeys(nodes_to_cure, 0)
    nx.set_node_attributes(G, nodes, name = 'Infection')    
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
    nodes = list({k:v for (k,v) in nx.get_node_attributes(G, 'Infection').items() if v!=0})
    return nodes

#Finds any nodes currently vaccinated in a graph
def find_vaccinated_nodes(G):
    nodes = list({k:v for (k,v) in nx.get_node_attributes(G, 'Vaccination').items() if v!=0})
    return nodes

#Finds any nodes currently healthy in a graph
def find_healthy_nodes(G):
    nodes = list({k:v for (k,v) in nx.get_node_attributes(G, 'Infection').items() if v==0})
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

def iteratorsuperfunc(repeats,graph,time_steps,show,log,delay,base_infection_strength,base_infection_decay,base_vacc_loss):
   ### initialisation###
   
   datalabels=['graph_tot','inf_list_tot','gross_inf_per_day_tot','net_inf_per_day_tot','inf_nodes_count_list_tot','R_sources_tot']
   
   ###GETTING THE DATA###
   graph_tot=[]
   inf_list_tot=[]
   gross_inf_per_day_tot=[]
   net_inf_per_day_tot=[]
   inf_nodes_count_list_tot=[]
   R_sources_tot=[]
   for i in range(repeats):
       graph, inf_list, gross_inf_per_day, net_inf_per_day, inf_nodes_count_list, R_sources = run_graph(graph, time_steps, show = show, log = log, delay = delay, base_infection_strength = base_infection_strength, base_infection_decay = base_infection_decay, base_vacc_loss = base_vacc_loss)
       graph_tot.append(graph)
       inf_list_tot.append(inf_list)
       gross_inf_per_day_tot.append(gross_inf_per_day)
       net_inf_per_day_tot.append(net_inf_per_day)
       inf_nodes_count_list_tot.append(inf_nodes_count_list)
       R_sources_tot.append(R_sources)
   data=[graph_tot,inf_list_tot,gross_inf_per_day_tot,net_inf_per_day_tot,inf_nodes_count_list_tot,R_sources_tot]
   for j in range(len(datalabels)):
       pd.DataFrame(data[i]).to_csv(datalabels[i])
      

#%% Utility

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


