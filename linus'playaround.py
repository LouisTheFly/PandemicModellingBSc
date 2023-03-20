#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 16:17:08 2023

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
def run_graph(G, time_steps = 20, show = False, log = False, delay = False, base_infection_strength = 5, base_infection_decay = 1, base_vacc_loss = 0.1):
    
    #Finds any infected nodes in the graph
    infected_nodes_list = [] #Contains a list of node keys infected at any point
    infected_nodes_list += find_infected_nodes(G) #Easier to read but not neccesary as 2 lines
    infected_nodes_count = len(infected_nodes_list) #Number of nodes infected at any point
    
    #Place to store count of each day's new infections
    net_infections_list = []
    gross_infections_list = []
    infected_nodes_count_list = []
    
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
        
        if len(infections_within_day) != 0:
            #Infect (Vaccinate) nodes and update overall list
            infect_nodes(G, infections_within_day, base_infection_strength)
            
            #Label source of infection attribute
            source_labels_dict = dict(zip(confirmed_infections, confirmed_sources))
            nx.set_node_attributes(G, source_labels_dict, name = 'Infected by:')   
            
        #Update overall infected list and remove duplicate nodes
        infected_nodes_list += infections_within_day
        infected_nodes_list = [*set(infected_nodes_list)]
        
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
    
    #For creating an R value
    R_sources = nx.get_node_attributes(G, 'Infected by:')
    R_sources = list(R_sources.values())
            
    return G, infected_nodes_list, gross_infections_list, net_infections_list, infected_nodes_count_list, R_sources

def run_graph(G,time):
    
    infected_nodes_set={}
    infected_nodes_set += find_infected_nodes(G)
    infected_count=len(infected_nodes_set)
    
    dangerous_nodes=np.array(infected_nodes_set)
    curing_nodes=[]
    
    #place to store days new infections and cures
    dailyinfcount=[]
    dailycurecount=[]
    Rnumber=[]
    daysinfected=np.array([0]*infected_count)
    source=np.array([])
    
    for i in tqdm(range(time)):
        daysinfected += 1
        intradaycure=[]
        intradayinf=[]

        for j in dangerous_nodes:
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
                    intradayinf += nodes_to_infect
                    source.append(source_nodes)
         
          
        #Take collated possible infections and check vaccination doesnt prevent infection
        if len(intradayinf) != 0:
            confirmed_infections = []
            confirmed_sources = []
            infections_subG = G.subgraph(intradayinf)
            
            #Find vaccination status
            vacc_status = nx.get_node_attributes(infections_subG, 'Vaccination')
            vacc_status = OrderedDict(sorted(vacc_status.items()))
            vacc_status_keys = np.array(list(vacc_status.keys()))
            vacc_status_vals = np.array(list(vacc_status.values()))

            #Run probability
            for i in range(len(intradayinf)):
                vacc_val = vacc_status_vals[np.where(vacc_status_keys == intradayinf[i])]
                if np.random.random() >= vacc_val:
                    confirmed_infections.append(intradayinf[i])
                    confirmed_sources.append(source_nodes[i])
            infections_within_day = confirmed_infections       
         
        if np.max(daysinfected)>=5:
            #this is stopping transmission
            locationinf=[]
            locationinf=np.where(daysinfected==5)[0]
            curing_nodes=dangerous_nodes[locationinf]
            dangerous_nodes=np.array(filter(lambda x: x not in curing_nodes, dangerous_nodes))
            stoptransmission_nodes(G,curing_nodes)
            numberinf=len(source[curing_nodes])
            rnumber=numberinf/len(curing_nodes)
            
        if np.max(daysinfected)>=10:
            #this is healing them
            print(daysinfected==10)
            locationcure=[]
            locationcure=np.where(daysinfected==10)[0]
            daysinfected=np.delete(daysinfected,locationcure)
            positive_nodes_list
            cure_nodes(G,locationcure)
    
    
#%%
def find_infected_nodes(G):
    nodes = set({k:v for (k,v) in nx.get_node_attributes(G, 'Infection').items() if v==True})
    return nodes
      
#Finds any nodes currently healthy in a graph
def find_healthy_nodes(G):
    nodes = list({k:v for (k,v) in nx.get_node_attributes(G, 'Infection').items() if v==False})
    return nodes
    
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

def stoptransmission_nodes(G, nodes_to_cure):
    nodes = dict.fromkeys(nodes_to_cure, False)
    nx.set_node_attributes(G, nodes, name = 'Infective')    
    return G

    
    
    
    
    
