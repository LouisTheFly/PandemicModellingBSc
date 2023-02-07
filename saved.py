#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 11:50:59 2023

@author: Linus
"""
import pandas as pd
import networkx as nx
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import graph_generator as gen
import copy

def infect_nodes(G, nodes_to_infect):
    nodes = dict.fromkeys(nodes_to_infect, True)
    nx.set_node_attributes(G, nodes, name = 'Infection')
    return G

def returninfections(graph,array_prob,nodes):
    infectionlist=(np.random.random(size=len(array_prob))<array_prob).astype(bool)
    infects=np.where(infectionlist)[0]
    infectednodes = [nodes[i] for i in infects]
    if np.any(infectednodes):
        graph=infect_nodes(graph,infectednodes)
        return infectednodes,graph
    else:
        return  [],graph
    
def remove_repeated(lst):
    return list(set(lst))

def plotting(x,y,title,xaxislabel,yaxislabel):
    plt.plot(x,y)
    plt.xlabel(xaxislabel)
    plt.ylabel(yaxislabel)
    plt.title(title)
    plt.grid()
    plt.show()

def rungraphalg(time,graph,infectedlist,infectionsperday):
   for i in range(time):
       #gen.draw_graph(graph, draw_type = 'circular')
       #plt.show()
       #print(infectedlist)
       infectionswithinday=[]
       for j in range(len(infectedlist)):
           x=infectedlist[j]
           nodes=list(nx.neighbors(graph,x))# CHCECK IF THESE ARE IN THE SAME ORDER
           nodes1=copy.deepcopy(nodes)
           nodes1.append(x)
           array_probabilities=nx.get_edge_attributes(nx.subgraph(graph,nodes1),'Probability') #produces a list of probabilities corresponding to each edge
           probs=list(array_probabilities.values())
           newinfections,graph=returninfections(graph,probs,nodes)
           if len(newinfections) > 0:
               infectionswithinday.append(len(newinfections))
               infectedlist.extend(newinfections)
               infectedlist=remove_repeated(infectedlist)
   infectionsperday.append(sum(infectionswithinday))
