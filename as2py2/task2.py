#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
'''
Assignment 2, Problem 2: Recomputing a Minimum Spanning Tree

Team Number:
Student Names: Li Ju,
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


# def update_MST_1(G, T, e, w):
#     """
#     Sig:  graph G(V,E), graph T(V, E), edge e, int ==>
#     Pre:
#     Post:
#     Ex:   TestCase 1 below
#     """
#     (u, v) = e
#     assert (e in G.edges() and e not in T.edges() and w > G[u][v]['weight'])
#
#     return T
#
#
# def update_MST_2(G, T, e, w):
#     """
#     Sig:  graph G(V,E), graph T(V, E), edge e, int ==>
#     Pre:
#     Post:
#     Ex:   TestCase 2 below
#     """
#     (u, v) = e
#     assert (e in G.edges() and e not in T.edges() and w < G[u][v]['weight'])
#
#
# def update_MST_3(G, T, e, w):
#     """
#     Sig:  graph G(V,E), graph T(V, E), edge e, int ==>
#     Pre:
#     Post:
#     Ex:   TestCase 3 below
#     """
#     (u, v) = e
#     assert (e in G.edges() and e in T.edges() and w < G[u][v]['weight'])
#     return T
#

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



class RecomputeMstTest(unittest.TestCase):
    """Test Suite for minimum spanning tree problem

    Any method named "test_something" will be run when this file is
    executed. Use the sanity check as a template for adding your own
    test cases if you wish.
    (You may delete this class from your submitted solution.)
    """

    def create_graph(self):
        G = nx.Graph()
        G.add_edge('a', 'b', weight=0.6)
        G.add_edge('a', 'c', weight=0.2)
        G.add_edge('c', 'd', weight=0.1)
        G.add_edge('c', 'e', weight=0.7)
        G.add_edge('c', 'f', weight=0.9)
        G.add_edge('a', 'd', weight=0.3)
        return G

    def draw_mst(self, G, T, n):
        if not have_plt:
            return
        pos = nx.spring_layout(G)  # positions for all nodes
        plt.subplot(220 + n)
        plt.title('updated MST %d' % n)
        plt.axis('off')
        # nodes
        nx.draw_networkx_nodes(G, pos, node_size=700)
        # edges
        nx.draw_networkx_edges(G, pos, width=6, alpha=0.5,
                               edge_color='b', style='dashed')
        nx.draw_networkx_edges(T, pos, width=6)
        # labels
        nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')

    # def test_mst1(self):
    #     """Sanity Test
    #
    #     This is a simple sanity check for your function;
    #     passing is not a guarantee of correctness.
    #     """
    #     # TestCase 1: e in G.edges() and not e in T.edges() and
    #     #             w > G[u][v]['weight']
    #     G = self.create_graph()
    #     T = nx.minimum_spanning_tree(G)
    #     update_MST_1(G, T, ('a', 'd'), 0.5)
    #     self.draw_mst(G, T, 1)
    #     self.assertItemsEqual(
    #         T.edges(),
    #         [('a', 'b'), ('a', 'c'), ('c', 'd'), ('c', 'e'), ('c', 'f')]
    #     )
    #
    # def test_mst2(self):
    #     # TestCase 2: e in G.edges() and not e in T.edges() and
    #     #             w < G[u][v]['weight']
    #     G = self.create_graph()
    #     T = nx.minimum_spanning_tree(G)
    #     update_MST_2(G, T, ('a', 'd'), 0.1)
    #     self.draw_mst(G, T, 2)
    #     self.assertItemsEqual(
    #         T.edges(),
    #         [('a', 'b'), ('a', 'd'), ('c', 'd'), ('c', 'e'), ('c', 'f')]
    #     )
    #
    # def test_mst3(self):
    #     # TestCase 3: e in G.edges() and e in T.edges() and
    #     #             w < G[u][v]['weight']
    #     G = self.create_graph()
    #     T = nx.minimum_spanning_tree(G)
    #     update_MST_3(G, T, ('a', 'c'), 0.1)
    #     self.draw_mst(G, T, 3)
    #     self.assertItemsEqual(
    #         T.edges(),
    #         [('a', 'b'), ('a', 'c'), ('c', 'd'), ('c', 'e'), ('c', 'f')]
    #     )

    def test_mst4(self):
        # TestCase 4: e in G.edges() and e in T.edges() and
        #             w > G[u][v]['weight']
        G = self.create_graph()
        T = nx.minimum_spanning_tree(G)
        update_MST_4(G, T, ('a', 'c'), 0.4)
        self.draw_mst(G, T, 4)
        self.assertItemsEqual(
            T.edges(),
            [('a', 'b'), ('a', 'd'), ('c', 'd'), ('c', 'e'), ('c', 'f')]
        )

    @classmethod
    def tearDownClass(cls):
        if have_plt:
            plt.show()


if __name__ == '__main__':
    unittest.main()