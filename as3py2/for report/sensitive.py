#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
'''
Assignment 3, Problem 1: Controlling the Maximum Flow

Team Number:   55
Student Names: Li Ju, Georgios
'''

'''
Copyright: Pierre.Flener@it.uu.se and his teaching assistants, 2019.

This file is part of course 1DL231 at Uppsala University, Sweden.

Permission is hereby granted only to the registered students of that
course to use this file, for a homework assignment.

The copyright notice and permission notice above shall be included in
all copies and extensions of this file, and those are not allowed to
appear publicly on the internet, both during a course instance and
forever after.
'''

import unittest

import networkx as nx
# API for NetworkX flow algorithms changed in v1.9:
if (list(map(lambda x: int(x), nx.__version__.split("."))) < [1, 9]):
    max_flow = nx.ford_fulkerson
else:
    max_flow = nx.maximum_flow
"""
We use max_flow() to generate flows for the included tests, and you
may of course use it as well in any tests you generate.  As always,
your implementation of the senstive() function may NOT make use of
max_flow(), or any of the other graph algorithm implementations
provided by NetworkX.
"""

# If your solution needs a queue (like the BFS algorithm), you can use this one:
from collections import deque

try:
    import matplotlib.pyplot as plt
    HAVE_PLT = True
except ImportError:
    HAVE_PLT = False

"""
F is represented in python as a dictionary of dictionaries;
i.e., given two nodes u and v,
the computed flow from u to v is given by F[u][v].
"""
def sensitive(G, s, t, F):
    """
    Sig:  graph G(V,E), int, int, int[0..|V|-1, 0..|V|-1] ==> int, int
    Pre:    G: a directed graph, in which every edge has its capacity;
            s: flow starts from node s; t: flow ends at node t;
            F: the given max flow matrix, in which flows each edge holds are stored
    Post:   return a sensitive edge by giving its starting node and ending node
    Ex:   sensitive(G,0,5,F) ==> (1, 3)
    """
    ## Function to construct residual graph of given graph with its flow
    def res_graph(Graph, Flow):
        """
        Sig:  graph G(V,E), int[0..|V|-1, 0..|V|-1] ==> graph eG(V, E)
        Pre:    G: a directed graph, in which every edge has its capacity;
                F: the given max flow matrix, in which flows each edge holds are stored
        Post:   return the residual graph of given graph and flow
        Ex:   res_graph(G,F) ==> rG
        """
        rG = Graph.copy()
        ## update the copy of original graph edge by edge
        for start_node in Flow:
            for end_node in Flow[start_node]:
                ## add the reversed edge with capacity of current flow
                rG.add_edge(end_node, start_node, capacity = Flow[start_node][end_node])
                ## update the original edge's capacity to original capacity minus flow
                rG[start_node][end_node]['capacity'] -= Flow[start_node][end_node]
        return rG

    ## build a function to explore all reachable nodes from a given node,
    ## reach_dict is the dictionary recording the reachable nodes,
    ## in which reachable nodes are marked as 1 while unreachable nodes are noted as -1
    def explore(G, node, reach_dict):
        """
        Sig:  graph G(V,E), int, dictionary ==> dictionary
        Pre:    G: a directed graph which is the residual flow graph for a graph and its flow;
                node: node we start to explore
                reach_dict: a dictionary in which all nodes are discovered or not from node
                are recorded
        Post:   return the dictionary in which every node are reachable or not are recorded:
                if reachable, it is noted as1 otherwise it's noted as -1
        Ex:   explore(G,s,reach_dict) ==> reach_dict
        """
        reach_dict[node] = 1
        ## a DFS-like approach, to explore each node directly linked with current node
        for each in G[node]:
            if G[node][each]['capacity'] > 0 and reach_dict[each] == -1:
                explore(G, each, reach_dict)
        return reach_dict

    ## construct the residual graph rG of given graph G
    rG = res_graph(G, F)
    ## build a the status dictionary and mark every node in rG as -1,
    ## which means unreachable (currently)
    reachable_dict = dict.fromkeys(list(rG.nodes), -1)
    ## explore the graph from the the node s, to find all reachable nodes
    reachable_dict = explore(rG, s, reachable_dict)

    ## find all saturated edges, whose capacity equals the flow it holds
    satur_edges = []
    for start_node in F:
        for end_node in F[start_node]:
            if F[start_node][end_node] == G[start_node][end_node]["capacity"]:
                satur_edges.append([start_node, end_node])

    ## NOTICE: not all saturated edges are sensitive edges -- only those which are in minimum
    ## cut are sensitive
    sens_edges = []
    for each in satur_edges:
        ## to find which saturated edges are among the minimum cut
        if reachable_dict[each[0]] == 1 and reachable_dict[each[1]] == -1:
            sens_edges.append(each)
    ## return any edge of sensitive edges: because of the theorem of maxflow-minicut, it is
    ## guaranteed that there is at least one edge is sensitive
    return sens_edges[0]

class SensitiveSanityCheck(unittest.TestCase):
    """
    Test suite for the sensitive edge problem
    """
    def draw_graph(self, H, u, v, flow1, F1, flow2, F2):
        if not HAVE_PLT:
            return
        pos = nx.spring_layout(self.G)
        plt.subplot(1,2,1)
        plt.axis('off')
        nx.draw_networkx_nodes(self.G,pos)
        nx.draw_networkx_edges(self.G,pos)
        nx.draw_networkx_labels(self.G,pos)
        nx.draw_networkx_edge_labels(
            self.G, pos,
            edge_labels={(u,v):'{}/{}'.format(
                  F1[u][v],
                  self.G[u][v]['capacity']
                ) for (u,v,data) in nx.to_edgelist(self.G)})
        plt.title('before: flow={}'.format(flow1))
        plt.subplot(1,2,2)
        plt.axis('off')
        nx.draw_networkx_nodes(self.G,pos)
        nx.draw_networkx_edges(self.G,pos)
        nx.draw_networkx_edges(
            self.G, pos,
            edgelist=[(u,v)],
            width=3.0,
            edge_color='b')
        nx.draw_networkx_labels(self.G,pos)
        nx.draw_networkx_edge_labels(
            self.G, pos,
            edge_labels={(u,v):'{}/{}'.format(
                  F2[u][v],H[u][v]['capacity']
                ) for (u,v,data) in nx.to_edgelist(self.G)})
        plt.title('after: flow={}'.format(flow2))

    def setUp(self):
        """start every test with an empty directed graph"""
        self.G = nx.DiGraph()

    def run_test(self, s, t, draw=False):
        """standard tests to run for all cases

        Uses networkx to generate a maximal flow
        """
        H = self.G.copy()
        # compute max flow
        flow_g, F_g = max_flow(self.G, s, t)
        # find a sensitive edge
        u,v = sensitive(self.G, s, t, F_g)
        # is u a node in G?
        self.assertIn(u, self.G, "Invalid edge ({}, {})".format(u ,v))
        # is (u,v) an edge in G?
        self.assertIn(v, self.G[u], "Invalid edge ({}, {})".format(u ,v))
        # decrease capacity of (u,v) by 1
        H[u][v]["capacity"] = H[u][v]["capacity"] - 1
        # recompute max flow
        flow_h, F_h = max_flow(H, s, t)
        if draw:
            self.draw_graph(H, u, v, flow_g, F_g, flow_h, F_h)
        # is the new max flow lower than the old max flow?
        self.assertLess(
            flow_h,
            flow_g,
            "Returned non-sensitive edge ({},{})".format(u,v))

    def test_sanity(self):
        """Sanity check"""
        # The attribute on each edge MUST be called "capacity"
        # (otherwise the max flow algorithm in run_test will fail).
        self.G.add_edge(0, 1, capacity = 16)
        self.G.add_edge(0, 2, capacity = 13)
        self.G.add_edge(2, 1, capacity = 4)
        self.G.add_edge(1, 3, capacity = 12)
        self.G.add_edge(3, 2, capacity = 9)
        self.G.add_edge(2, 4, capacity = 14)
        self.G.add_edge(4, 3, capacity = 7)
        self.G.add_edge(3, 5, capacity = 20)
        self.G.add_edge(4, 5, capacity = 4)
        self.run_test(0,5,draw=True)

    @classmethod
    def tearDownClass(cls):
        if HAVE_PLT:
            plt.show()

if __name__ == "__main__":
    unittest.main()
