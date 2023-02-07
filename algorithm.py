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
