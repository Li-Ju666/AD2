#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
'''
Assignment 2, Problem 1: Search String Replacement

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

# Sample matrix provided by us:
from string import ascii_lowercase

# Solution to Task B:
def min_difference(u,r,R):
    """
    Sig:  string, string, int[0..|A|, 0..|A|] ==> int
    Pre:  u and r are strings to be compared, while R is the resemblance matrix
    Post: the function returns the minimal differences between two given strings
    Ex:   Let R be the resemblance matrix where every change and skip costs 1
          min_difference("dinamck","dynamic",R) ==> 3
    """
    # To get the resemblance between two letters, use code like this:
    # difference = R['a']['b']
    A = [[None for i in range(len(r))+1] for j in range(len(u)+1)]
    def min_dif(i, j):
        if A[i+1][j+1] is None:
            if i == 0 or j == 0:
                result = abs(i-j)
            else:
                result = min(
                    min_dif(i-1, j)+R[u[i]]['-'],
                    min_dif(i, j-1)+R['-'][r[j]],
                    min_dif(i-1, j-1)+R[u[i]][r[j]]
                )
            A[i+1][j+1] = result
        else: result = A[i+1][j+1]
        return result
    A[len(u)][len(j)] = min_dif(len(u)-1, len(r)-1)
    return A[len(u)][len(j)]

# Solution to Task C:
def min_difference_align(u,r,R):
    """
    Sig:  string, string, int[0..|A|, 0..|A|] ==> int, string, string
    Pre:
    Post:
    Ex:   Let R be the resemblance matrix where every change and skip costs 1
          min_difference_align("dinamck","dynamic",R) ==>
                                    3, "dinam-ck", "dynamic-"
    """

def qwerty_distance():
    """Generates a QWERTY Manhattan distance resemblance matrix

    Costs for letter pairs are based on the Manhattan distance of the
    corresponding keys on a standard QWERTY keyboard.
    Costs for skipping a character depends on its placement on the keyboard:
    adding a character has a higher cost for keys on the outer edges,
    deleting a character has a higher cost for keys near the middle.

    Usage:
        R = qwerty_distance()
        R['a']['b']  # result: 5
    """
    from collections import defaultdict
    import math
    R = defaultdict(dict)
    R['-']['-'] = 0
    zones = ["dfghjk", "ertyuislcvbnm", "qwazxpo"]
    keyboard = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
    for num, content in enumerate(zones):
        for char in content:
            R['-'][char] = num + 1
            R[char]['-'] = 3 - num
    for a in ascii_lowercase:
        rowA = None
        posA = None
        for num, content in enumerate(keyboard):
            if a in content:
                rowA = num
                posA = content.index(a)
        for b in ascii_lowercase:
            for rowB, contentB in enumerate(keyboard):
                if b in contentB:
                    R[a][b] = int(math.fabs(rowB - rowA) + math.fabs(posA - contentB.index(b)))
    return R

class MinDifferenceTest(unittest.TestCase):
    """Test Suite for search string replacement problem

    Any method named "test_something" will be run when this file is
    executed. Use the sanity check as a template for adding your own test
    cases if you wish.
    (You may delete this class from your submitted solution.)
    """

    def test_diff_sanity(self):
        """Difference sanity test

        Given a simple resemblance matrix, test that the reported
        difference is the expected minimum. Do NOT assume we will always
        use this resemblance matrix when testing!
        """
        alphabet = ascii_lowercase + '-'
        # The simplest (reasonable) resemblance matrix:
        R = dict( [ (
                     a,
                     dict( [ ( b, (0 if a==b else 1) ) for b in alphabet ] )
                    ) for a in alphabet ] )
        # Warning: we may (read: 'will') use another matrix!
        self.assertEqual(min_difference("dinamck","dynamic",R),3)
    def test_align_sanity(self):
        """Simple alignment

        Passes if the returned alignment matches the expected one.
        """
        # QWERTY resemblance matrix:
        R = qwerty_distance()
        diff, u, r = min_difference_align("polynomial", "exponential", R)
        # Warning: we may (read: 'will') use another matrix!
        self.assertEqual(diff, 15)
        # Warning: there may be other optimal matchings!
        self.assertEqual(u, '--polyn-om-ial')
        self.assertEqual(r, 'exp-o-ne-ntial')

if __name__ == '__main__':
    unittest.main()