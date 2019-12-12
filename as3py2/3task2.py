#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
'''
Assignment 3, Problem 2: Party Seating

Team Number:   
Student Names: 
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
    Pre:  
    Post: [1, 2, 3][0, 2][0, 1][0]
    Ex:   [[1,2],[0],[0]] ==> True, [0], [1,2]
    """
    status_dict = dict.fromkeys(range(len(known)), 0)
    result = True
    unarranged_dict = dict.fromkeys(range(len(known)), 0)
    def arrange(node, parent):
        print('Now checking:', node)
        unarranged_dict.pop(node)
        if parent is None:
            status_dict[node] = 1
            linked_nodes = known[node]
        else:
            status_dict[node] = -status_dict[parent]
            linked_nodes = known[node]
            print('linked_nodes', linked_nodes)
            linked_nodes.remove(parent)

        print(linked_nodes)
        result = True
        if linked_nodes is not None:
            for each in linked_nodes:
                if result == True:
                    if status_dict[each] == status_dict[node]:
                        print('ops this wont work!')
                        result = False
                    elif status_dict[each] == 0:
                        result = arrange(each, node)
                    else: print("already found and nothing happens!")
        return result

    while result is True and len(unarranged_dict) > 0:
        print('currently guest', unarranged_dict.keys()[0], 'is being checked!')
        result = arrange(unarranged_dict.keys()[0], None)
    table1, table2 = [], []
    if result == True:
        for each in status_dict:
            if status_dict[each] == 1:
                table1.append(each)
            else: table2.append(each)
    print(result, table1, table2)
    return result, table1, table2

known = [[3, 4, 5, 1], [3, 4, 5, 0], [3, 4, 5], [0, 1, 2], [0, 1, 2], [0,1, 2]]
print(party(known))