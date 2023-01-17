#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 14:29:14 2023

@author: Linus
"""

import networkx as nx
import numpy as np
import scipy as sp
from collections import deque
#%%

"""
Here’s how it works:

Initially, queue contains a single element, source, and dist maps from source to distance 0 (which is the distance from source to itself).

Each time through the loop, we use popleft to select the next node in the queue.

Next we find all neighbors of node that are not already in dist.

Since the distance from source to node is dist[node], the distance to any of the undiscovered neighbors is dist[node]+1.

For each neighbor, we add an entry to dist, then we add the neighbors to the queue.

This algorithm only works if we use BFS, not DFS. To see why, consider this:

The first time through the loop node is source, and new_dist is 1. So the neighbors of source get distance 1 and they go in the queue.

When we process the neighbors of source, all of their neighbors get distance 2. We know that none of them can have distance 1, because if they did, we would have discovered them during the first iteration.

Similarly, when we process the nodes with distance 2, we give their neighbors distance 3. We know that none of them can have distance 1 or 2, because if they did, we would have discovered them during a previous iteration.
"""
def shortest_path_dijkstra(G, source):
    dist = {source: 0}
    queue = deque([source])
    while queue:
        node = queue.popleft()
        new_dist = dist[node] + 1
        neighbors = set(G[node]).difference(dist)
        for n in neighbors:
            dist[n] = new_dist

        queue.extend(neighbors)
    return dist