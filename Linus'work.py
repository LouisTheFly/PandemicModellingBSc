#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 13:26:14 2023

@author: Linus
"""

import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
 
#%%
#Create a network of 100 individuals
G = nx.complete_graph(100)
 
#Initialize each individual with a randomly assigned 'susceptibility' to the virus
for n in G.nodes():
    G.nodes[n]['susceptible'] = random.randint(1, 10)
 
#Simulate the spread of the virus
for n in G.nodes():
    if G.nodes[n]['susceptible'] > 6:
        G.nodes[n]['infected'] = True
    else:
        G.nodes[n]['infected'] = False
 
#Mark each node as 'infected' if it is connected to an infected node
for x, y in G.edges():
    if G.nodes[x]['infected'] == True or G.nodes[y]['infected'] == True:
        G.nodes[x]['infected'] = True
        G.nodes[]
        
        
#%%


import networkx as nx
import matplotlib.pyplot as plt
import random

# Create a graph
G = nx.cycle_graph(6) 

# Create a list of nodes
nodes = list(G.nodes())

# Select a random node as the infected node
infected_node = random.choice(nodes)

# Iterate over the remaining nodes and generate edges
for node in nodes:
    # Generate a random number
    r = random.random()
    # If it is greater than 0.5, create an edge between the infected node and current node
    if r > 0.5:
        G.add_edge(infected_node, node)

# Visualize the graph
plt.figure()
nx.draw(G, with_labels=True, font_weight='bold')
plt.show()

#%%


import networkx as nx 
import matplotlib.pyplot as plt 

# Create a graph 
G = nx.Graph() 

# Add nodes 
G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_node(4)
G.add_node(5)

# Add edges 
G.add_edge(1,2)
G.add_edge(1,3)
G.add_edge(2,3)
G.add_edge(2,4)
G.add_edge(3,4)
G.add_edge(3,5)
G.add_edge(4,5)

# Visualize the graph 
nx.draw(G, with_labels=True)
plt.show()

# Simulate pandemic 
# Let node 1 be the infected node 
infected_nodes = [1]

# Iterate over each edge in the graph 
for edge in G.edges(): 
    # If the source node is infected 
    if edge[0] in infected_nodes: 
        # Infect the target node 
        infected_nodes.append(edge[1]) 

# Print the list of infected nodes 
print("Infected nodes:", infected_nodes)

#%%

import networkx as nx
import matplotlib.pyplot as plt

# create a network graph
G = nx.Graph()

# add nodes 
G.add_node('Person 0')

# add edges
G.add_edge('Person 0', 'Person 1')
G.add_edge('Person 0', 'Person 2')
G.add_edge('Person 0', 'Person 3')
G.add_edge('Person 0', 'Person 4')
G.add_edge('Person 0', 'Person 5')

# draw the graph
nx.draw(G, node_size = 1000, node_color = 'orange')
plt.show()

# simulate the spread of the virus
# Person 0 is sick
infected = ['Person 0']

# Persons 1-5 can get sick
susceptible = ['Person 1', 'Person 2', 'Person 3', 'Person 4', 'Person 5']

# Create an empty list to store the infected people
while len(susceptible) > 0:
    new_infected = []

    # Infect the susceptible people
    for person in susceptible:
        if 'Person 0' in G.neighbors(person):
            new_infected.append(person)

    # Remove the newly infected people from the susceptible list
    for person in new_infected:
        susceptible.remove(person)

    # Add the newly infected people to the infected list
    for person in new_infected:
        infected.append(person)

# Visualize the infection
nx.draw(G, node_size = 1000, nodelist=infected, node_color = 'red')
plt.show()

#%%

import networkx as nx 
import matplotlib.pyplot as plt 

#create a graph 
G = nx.Graph() 

#add the first node
G.add_node(1, health_status="infected")

#add other nodes 
for i in range(2,11):
    G.add_node(i, health_status="healthy")

#add edges
G.add_edges_from([(1,2), (1,3), (2,3), (2,4), (3,4), (3,5), (4,5), (4,6),
                 (5,6), (5,7), (6,7), (6,8), (7,8), (7,9), (8,9), (8,10),
                  (9,10)])

#draw the graph 
#color nodes based on their health status 
colors = []
for node in G.nodes():
    if G.nodes[node]['health_status'] == 'infected':
        colors.append('red')
    else:
        colors.append('blue')

nx.draw(G, node_color=colors, with_labels=True)
plt.show()

#simulate the spread of the disease
#assume that each node has a 10% chance of getting infected 
for node in G.nodes():
    if G.nodes[node]['health_status'] == 'healthy':
        if random.random() <= 0.1:
            G.nodes[node]['health_status'] = 'infected'
            colors[node-1] = 'red'

#re-draw the graph
nx.draw(G, node_color=colors, with_labels=True)
plt.show()

#%%
"""
All above were CHATGPT trials, here we are stress testing networks.
How large can we generate with the computational power we have
Try creating a graph with enough nodes to represent a population
Find largest population that can be created visually and non-visually
IN time of around 30 seconds
"""
node_names = np.arange(1000)
graph = nx.DiGraph()
for i in node_names:
    graph.add_node('%s'%i)
graph.add_edge('2','3')
#nx.draw_random(graph, with_labels = True)
"""
very challenging to visualise anything over 1000

without visualisation it can run 1 million nodes with ease
a 10 million node graph takes around 1 or 2 minutes to generate
"""

#%%
"""
Functions to generate regular graphs
"""