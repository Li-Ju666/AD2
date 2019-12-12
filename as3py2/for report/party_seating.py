#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
'''
Assignment 3, Problem 2: Party Seating

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

# If your solution needs a queue, then you can use this one:
from collections import deque

def party(known):
    """
    Sig:  int[1..m, 1..n] ==> boolean, int[1..j], int[1..k]
    Pre:  a list of list, in which stored the edges between nodes
    Post: a boolean indicating if such arrangement can be made, if True, two list containing the plan are returned,
          otherwise two empty lists are returned.
    Ex:   [[1,2],[0],[0]] ==> True, [0], [1,2]
    """
    ## construct a dictionary to store the current status of every node, 0 means the node has not been arranged,
    ## 1 means it is set in the list1, while -1 means it is set in the list2. The initial status is all nodes are 0.
    status_dict = dict.fromkeys(range(len(known)), 0)

    ## A dictionary for storage of unarranged nodes:
    ## the reason for using dictionary instead of list is that the complexity of dictionary's deletion is of constant time,
    ## removal of an arranged node requires operated |nodes| times, this is used for reduction of time complexity.
    unarranged_dict = dict.fromkeys(range(len(known)), 0)

    ## The default result if such arrangement is available is True
    result = True

    ## the function arrange is defined to arrange the given node and its children recursively
    def arrange(node, parent):
        # print('Now checking:', node)

        ## update the status of current node in status_dictionary according to its parent's status: opposite to its
        ## parent's status
        if parent is None:
            status_dict[node] = 1
            linked_nodes = known[node]
        else:
            status_dict[node] = -status_dict[parent]
            linked_nodes = known[node]
            # print('linked_nodes', linked_nodes)
            linked_nodes.remove(parent)
        # print('children node: ', linked_nodes)

        ## delete the current node from dictionary of unarranged nodes
        unarranged_dict.pop(node)

        ## The default result if such arrangement is available is True, if every node is put with no contradiction,
        ## it keeps True
        result = True

        ## arrange given node's children
        if linked_nodes is not None:
            for each in linked_nodes:
                ## if contradiction occurs, end the loop
                if result == True:
                    ## a child's status equals its own status: contradiction occurs
                    if status_dict[each] == status_dict[node]:
                        result = False
                    ## the child has not been arranged: recursively arrange the child
                    elif status_dict[each] == 0:
                        result = arrange(each, node)
        return result

    ## arrange all the unarranged nodes: if contradiction occurs, end the loop
    while result is True and len(unarranged_dict) > 0:
        result = arrange(unarranged_dict.keys()[0], None)
    table1, table2 = [], []
    if result == True:
        ## traverse the status dictionary: nodes whose value are 1 is put in list1, while those whose value is -1
        ## are appended in list2
        for each in status_dict:
            if status_dict[each] == 1:
                table1.append(each)
            else: table2.append(each)
    return result, table1, table2

class PartySeatingTest(unittest.TestCase):
    """Test suite for party seating problem
    """

    def test_sanity(self):
        """Sanity test

        A minimal test case.
        """
        K = [[1,2],[0],[0]]
        (found, A, B) = party(K)
        self.assertEqual(
            len(A) + len(B),
            len(K),
            "wrong number of guests: {!s} guests, tables hold {!s} and {!s}".format(
                len(K),
                len(A),
                len(B)
                )
            )
        for g in range(len(K)):
            self.assertTrue(
                g in A or g in B,
                "Guest {!s} not seated anywhere".format(g))
        for a1 in A:
            for a2 in A:
                self.assertFalse(
                    a2 in K[a1],
                    "Guests {!s} and {!s} seated together, and know each other".format(
                        a1,
                        a2
                        )
                    )
        for b1 in B:
            for b2 in B:
                self.assertFalse(
                    b2 in K[b1],
                    "Guests {!s} and {!s} seated together, and know each other".format(
                        b1,
                        b2
                        )
                    )

if __name__ == '__main__':
    unittest.main()
