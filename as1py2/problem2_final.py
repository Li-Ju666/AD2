import networkx as nx
import matplotlib
import random
import unittest


def ring(G):
    result = False
    discovered = []
    undiscovered = list(G.nodes)
    parent_dic = {}

    def explore(node, parent):

        if node not in discovered:
            result = False
            parent_dic[node] = parent
            discovered.append(node)
            undiscovered.remove(node)

            adj = list(G.adj[node])

            if parent is not None:
                adj.remove(parent)

            discovered_again = []

            for element in adj:
                if element in parent_dic.keys():
                    discovered_again.append(element)

            if len(discovered_again) != 0:
                print("RING FOUND! ")
                return True
            else:
                for i in adj:
                    if result is False:
                        result = explore(i, node)

                return result

    while (len(undiscovered) != 0 and result is False):
        start_node = random.choice(undiscovered)
        result = explore(start_node, None)
    return result





# def ring_extended(G):
#     result = False
#     discovered = []
#     undiscovered = list(G.nodes)
#     parent_dic = {}
#     ring_elements = []
#
#     def explore(node, parent):
#         result = False
#         if node not in discovered:
#
#             discovered.append(node)
#             parent_dic[node] = parent
#             undiscovered.remove(node)
#
#             adj = list(G.adj[node])
#
#             if parent is not None:
#                 adj.remove(parent)
#
#             discovered_again = []
#
#             for element in adj:
#                 if element in parent_dic.keys():
#                     discovered_again.append(element)
#
#             if len(discovered_again) != 0:
#                 print("RING FOUND! ")
#                 ring_elements.append(random.choice(discovered_again))
#                 ring_elements.append(node)
#                 return True
#             else:
#                 for i in adj:
#                     if result is False:
#                         result = explore(i, node)
#                 return result
#
#     while (len(undiscovered) != 0 and result is False):
#         start_node = random.choice(undiscovered)
#         result = explore(start_node, None)
#     if (result is True):
#         i = 1
#         while ring_elements[i] != ring_elements[0]:
#             ring_elements.append(parent_dic[ring_elements[i]])
#             i = i + 1
#     return result, ring_elements

def ring_extended(G):
    result = False
    undiscovered = list(G.nodes)
    parent_dic = {}
    ring_elements = []

    def explore(node, parent):
        result = False
        if node not in parent_dic.keys():
            parent_dic[node] = parent
            undiscovered.remove(node)

            adj = list(G.adj[node])

            if parent is not None:
                adj.remove(parent)

            discovered_again = []

            for element in adj:
                if element in parent_dic.keys():
                    discovered_again.append(element)

            if len(discovered_again) != 0:
                print("RING FOUND! ")
                ring_elements.append(random.choice(discovered_again))
                ring_elements.append(node)
                return True
            else:
                for i in adj:
                    if result is False:
                        result = explore(i, node)
                return result

    while (len(undiscovered) != 0 and result is False):
        start_node = random.choice(undiscovered)
        result = explore(start_node, None)
    if (result is True):
        i = 1
        while ring_elements[i] != ring_elements[0]:
            ring_elements.append(parent_dic[ring_elements[i]])
            i = i + 1
    return result, ring_elements


class RingTest(unittest.TestCase):
    """Test Suite for ring detection problem

    Any method named "test_something" will be run when this file is
    executed. Use the sanity check as a template for adding your own test
    cases if you wish.
    (You may delete this class from your submitted solution.)
    """

    def is_ring(self, graph, path):
        """Asserts that the nodes in path from a ring in graph"""
        traversed = nx.Graph()
        for v in range(len(path) - 1):
            self.assertTrue(
                path[v + 1] in graph.neighbors(path[v]),
                "({},{}) is not an edge in the graph\ngraph: {}".format(
                    path[v],
                    path[v + 1],
                    graph.edges())
            )
            self.assertFalse(
                traversed.has_edge(path[v], path[v + 1]),
                "duplicated edge: ({},{})".format(path[v], path[v + 1]))
            traversed.add_edge(path[v], path[v + 1])
        self.assertEqual(
            path[0], path[-1],
            "start and end not equal: {} != {}".format(path[0], path[-1]))

    def test_sanity(self):
        """Sanity Test

        This is a simple sanity check for your function;
        passing is not a guarantee of correctness.
        """
        testgraph = nx.Graph([(0, 1), (0, 2), (0, 3), (2, 4), (2, 5), (3, 6), (3, 7), (7, 8), (8, 3)])
        self.assertTrue(ring(testgraph))
        testgraph.add_edge(6, 8)
        self.assertTrue(ring(testgraph))

    def test_extended_sanity(self):
        """sanity test for returned ring"""
        testgraph = nx.Graph([(0, 1), (0, 2), (0, 3), (2, 4), (2, 5), (3, 6), (3, 7), (7, 8), (6, 8)])
        found, thering = ring_extended(testgraph)
        self.assertTrue(found)
        self.is_ring(testgraph, thering)
        print(thering)
        # Uncomment to visualize the graph and returned ring:
        #draw_graph(testgraph, thering)


if __name__ == '__main__':
    unittest.main()