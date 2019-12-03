#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
'''
Assignment 2, Problem 1: Search String Replacement

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
    A = [[None for i in range(len(r)+1)] for j in range(len(u)+1)]  ## Result matrix with initial values of None
    def min_dif(i, j):
        ## the funtion to return the result of subproblem:
        ## if the result existing in the matrix, return the value from matrix A;
        ## if not, calculate the matrix recursively, and save the value in the matrix A
        if i < 0 or j < 0: result = float('inf')
        ## if the length of one sub_string (eg. i) to be compared reduce to 0 while another does not,
        # value 'inf' forces recursive function goes to case in which j = j-1 and i keeps 0.
        elif A[i][j] is None:
            ## if both strings reduce to empty, return distance between '-' and '-'
            if i == 0 and j == 0:
                result = R['-']['-']
            else:
                ## According to the OPT, optimal choice is the minimal of these 3 cases
                result = min(
                    min_dif(i - 1, j) + R[u[i - 1]]['-'],
                    min_dif(i, j - 1) + R['-'][r[j - 1]],
                    min_dif(i - 1, j - 1) + R[u[i - 1]][r[j - 1]])
            A[i][j] = result
        else: result = A[i][j]
        return result
    ## calculate the result of the entire problem, subproblems will be calculated and
    ## results will be stored in matrix A.
    A[len(u)][len(r)] = min_dif(len(u), len(r))
    return A[len(u)][len(r)]

# Solution to Task C:
def min_difference_align(u,r,R):
    """
    Sig:  string, string, int[0..|A|, 0..|A|] ==> int, string, string
    Pre: u and r are strings to be compared, while R is the resemblance matrix
    Post: the function returns the minimal differences between two given strings, and the positioning for the
          minimum differences.
    Ex:   Let R be the resemblance matrix where every change and skip costs 1
          min_difference_align("dinamck","dynamic",R) ==>
                                    3, "dinam-ck", "dynamic-"
    """
    ## Matrix A is the result matrix, as it acts in the previous function.
    A = [[None for i in range(len(r)+1)] for j in range(len(u)+1)]
    def min_dif(i, j):

        ## if both strings reduce to empty, return distance between '-' and '-'
        if i < 0 or j < 0: result = float('inf')
        ## if the length of one sub_string (eg. i) to be compared reduce to 0 while another does not,
        # value 'inf' forces j = j-1 and i keeps 0.
        elif A[i][j] is None:
            if i == 0 and j == 0:
                result = R['-']['-']
            else:
                result = min(
                    min_dif(i - 1, j) + R[u[i - 1]]['-'],
                    min_dif(i, j - 1) + R['-'][r[j - 1]],
                    min_dif(i - 1, j - 1) + R[u[i - 1]][r[j - 1]])
            A[i][j] = result
        else: result = A[i][j]
        return result

    ## function trace_letter aims to return letters and hyphens of two strings one by one, to show the positioning of
    ## minimum differences by tracing result matrix A.
    def trace_letter(i, j):
        if i < 1 or j < 1:
            ## if edge of matrix reached (one of i and j is 0, eg. i = 0 and j is not),
            ## for the 1st string, return j hyphens and for the 2nd string, return first jth chars of original string.
            checked_u = j*'-' + u[:i]
            checked_r = i*'-' + r[:j]
        else:
            ## list cases contains three different cases and variable true_case indicates from which case value in
            ## current position is (in another word, which case has the minimum value)
            cases = (A[i - 1][j] + R[u[i - 1]]['-'], A[i][j - 1] + R['-'][r[j - 1]],
                          A[i - 1][j - 1] + R[u[i - 1]][r[j - 1]])
            true_case = cases.index(min(cases))
            ## In different cases, recursion path is different, following the previous OPT
            if true_case == 0:
                checked_u, checked_r = trace_letter(i - 1, j)
                checked_u = checked_u + u[i - 1]
                checked_r = checked_r + '-'
            elif true_case == 1:
                checked_u, checked_r = trace_letter(i, j - 1)
                checked_u = checked_u + '-'
                checked_r = checked_r + r[j - 1]
            else:
                checked_u, checked_r = trace_letter(i - 1, j - 1)
                checked_u = checked_u + u[i - 1]
                checked_r = checked_r + r[j - 1]
        return checked_u, checked_r

    A[len(u)][len(r)] = min_dif(len(u), len(r))
    checked_u, checked_r = trace_letter(len(u), len(r))

    return A[len(u)][len(r)], checked_r, checked_u


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