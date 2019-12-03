#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
'''
Assignment 2, Problem 2: Recomputing a Minimum Spanning Tree

Team Number:   55
Student Names: Li Ju and Georgios Panayiotou
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
"""IMPORTANT:
We're using NetworkX (version 1.11!) only to provide a reliable graph
object.  Your solution may NOT rely on the NetworkX implementation of
any graph algorithms.  You can use the node/edge creation functions to
create test data, and you can access node lists, edge lists, adjacency
lists, etc.  DO NOT turn in a solution that uses a NetworkX
implementation of a graph traversal algorithm, as doing so will result
in a score of 0.
"""

try:
    import matplotlib.pyplot as plt
    have_plt = True
except:
    have_plt = False

def update_MST_1(G, T, e, w):
    """
    Sig:  graph G(V,E), graph T(V, E), edge e, int ==> 
    Pre:  
    Post: 
    Ex:   TestCase 1 below
    """
    (u, v) = e
    assert(e in G.edges() and e not in T.edges() and w > G[u][v]['weight'])

def update_MST_2(G, T, e, w):
    """
    Sig:  graph G(V,E), graph T(V, E), edge e, int ==> 
    Pre:  
    Post: 
    Ex:   TestCase 2 below
    """
    (u, v) = e
    assert(e in G.edges() and e not in T.edges() and w < G[u][v]['weight'])

def update_MST_3(G, T, e, w):
    """
    Sig:  graph G(V,E), graph T(V, E), edge e, int ==> 
    Pre:  
    Post: 
    Ex:   TestCase 3 below
    """
    (u, v) = e
    assert(e in G.edges() and e in T.edges() and w < G[u][v]['weight'])

def update_MST_4(G, T, e, w):
    """
    #     Sig:  graph G(V,E), graph T(V, E), edge e, int ==> graph G with updated edge e, updated graph T (MST of G)
    #     Pre: A connected graph G, a subgraph T, which is the minimum spanning tree (MST) of G, an edge e to be
               updated which is in both G and T with a weight w greater than original weight of e.
    #     Post: Through this function, the given G is updated with given edge e firstly;
                also the MST T of updated graph G is recomputed.
    #     Ex:   TestCase 4 below
    #     """
    (u, v) = e
    ## To check if given e is satisfied with the case:
    assert (e in G.edges() and e in T.edges() and w > G[u][v]['weight'])

    ## To update G with given edge e
    G.add_edge(*e, weight = w)

    ## remove the changed edge, for it is not guaranteed to be in the MST
    T.remove_edge(u, v)
    # print(list(T.edges))
    # print(list(T.adj['a']))

    ## To provide a DFS function within a connected graph, returning all nodes
    def explore(node, parent):
        block = [node]
        son = list(T.adj[node])
        if parent is not None:
            son.remove(parent)

        for each in son:
            block = block + explore(each, node)
        return block

    ## To use DFS to find out two connected blocks of T (T split into 2 blocks for the deletion of e between node u and v)
    block1 = explore(u, None)
    block2 = explore(v, None)
    # print('block1 contains nodes: ', block1)
    # print('block2 contains nodes: ', block2)

    ## To define a dictionary, in which nodes in block 1 are noted as -1, while nodes in block 2 are noted as -1
    dic = dict.fromkeys(block1, -1)
    dic.update(dict.fromkeys(block2, 1))
    # print('dictionary is: ', dic)

    ## To find the cut_set between two blocks
    edges = list(G.edges)
    cut_set = []
    ## For those edges, whose two nodes are in different blocks, the sum of dictionary values of two nodes are exactly 0
    for each in edges:
        if dic[each[0]]+dic[each[1]] == 0:
            cut_set.append(each)
    # print(type(cut_set[0]))

    ## To find the minimum edge from the cut set between two blocks
    weight = []
    for each in cut_set:
        weight.append(G.edges[each]['weight'])
    # print(weight)

    ## add the minimum edge into graph T, which is the recomputed MST of updated G
    T.add_edge(*cut_set[weight.index(min(weight))], weight = min(weight))
    return None

