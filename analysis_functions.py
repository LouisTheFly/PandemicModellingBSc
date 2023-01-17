# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 14:17:38 2023

@author: Louis

"""
#Import Modules
import numpy as np
import scipy as sp
import networkx as nx
import matplotlib.pyplot as plt

#%%

#Takes graph name
#Returns an array containing every node with its corresponding degree
def degree_finder(graph):
    return graph.degree(graph.nodes)

#Takes array of nodes
#Returns histogram of node degrees
def degree_hist(nodes):
    degree_numbers = np.transpose(nodes)
    plt.hist(degree_numbers[1], bins = max(degree_numbers[1]))
    plt.show()
    return