#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 18:05:26 2020

@author: elianajn
@author: andrewpinkham
@author: will-pasley
"""
import pandas as pd
import re
import heapq
import numpy as np
from HashTable import HashTable
from LinkedList import LinkedList

class Problem():

    def __init__(self, _problem_num, _threshold, _items):
        self.problem_num = _problem_num
        self.threshold = _threshold
        self.items = _items

    def prt(self):
        print("num: {}".format(self.problem_num))
        print("threshold: {}".format(self.threshold))
        print("items: {}".format(self.items))
        print("--------------------------------------------")
        print(" ")

class Solver():

    def __init__(self, method):
        self.method = method

    def solve(self, problem):
        if self.method == "BRUTE_FORCE":
            return self.brute_force(problem)
        elif self.method == "DYNAMIC":
            return self.dynamic(problem)

    def brute_force(self, problem):
        out = self.sub_lists(list(problem.items.keys()))
        valid = []
        for l in out:
            weight_total = 0
            value_total = 0
            for key in l:
                weight_total += problem.items[key][1]
                value_total += problem.items[key][0]
            if weight_total <= problem.threshold:
                valid.append((l, value_total))
        valid.sort(key=lambda x:x[1])
        return valid[-1]

    def dynamic(self, problem):
        width = int(problem.threshold) + 1
        height = problem.items.size()
        matrix = np.zeros((height, width))
        # sortedItems is a list of tuples (weight,item)
        sortedItems = self.sortItems(problem)
        # number of columns is the total weight
        # number of rows is the number of items
        for row in range(problem.items.size()):
            for col in range(width):
                (valueS, weightS) = problem.items.get(sortedItems[row])
                value = int(valueS)
                weight = int(weightS)
                if row == 0:
                    if weight <= col:
                        matrix[row][col] = value
                    else:
                        matrix[row][col] = 0
                else:
                    if weight > col:
                        matrix[row][col] = matrix[row-1][col]
                    else:
                        score_above = matrix[row-1][col]
                        best_possible_score = value + matrix[row-1][col-weight]
                        matrix[row][col] = np.max([score_above, best_possible_score])
        # now we gotta select the items that actually got used
        # start at bottom right
        c = problem.threshold
        selected_items = []
        for r in range(height-1, -1, -1):
            # if the value is the same as the value above it that means that row item was not used
            if r != 0 and matrix[r][c] == matrix[r-1][c]:
                continue
            # if the one directly above is different decrement the column by the weight of the item being counted
            if r != 0 and matrix[r][c] != matrix[r-1][c]:
                item = sortedItems[r]
                selected_items.append(item)
                value, weight = problem.items.get(item)
                c -= int(weight)
                if c < 0:
                    break
            # if the row is 0 you can't look above. just consider the remaining weight
            elif r == 0:
                item = sortedItems[r]
                value, weight = problem.items.get(item)
                weight = int(weight)
                if weight <= c:
                    selected_items.append(item)
        return selected_items


    # sorts the list of items by decreasing weight
    def sortItems(self, problem):
        output = []
        c = 0
        keys = problem.items.getKeys()
        for key in keys:
            valueS, weightS = problem.items.get(key)
            value = int(valueS)
            weight = int(weightS)
            output.append([])
            output[c].append(weight)
            output[c].append(key)
            c += 1
        output.sort(key=lambda x:x[0])

        # since this is a bottom up method if there are multiple items with the same weight
        # we need to manually sort them so that the item with the larger value is later in the list
        for idx,item in enumerate(output):
            if item == output[0]:
                continue
            if item[0] == output[idx-1]:
                value_item = problem.items.get(item[1])
                value_backone = problem.items.get(output[idx-1][1])
                if value_item < value_backone:
                    output[idx], output[idx-1] = output[idx-1], output[idx]
        return(list(map(lambda x:x[1], output)))


def preprocess(file_name):
    # partition the dataset and return a list of problems
    file = pd.read_csv(file_name, header=None, encoding='utf-8')
    num_problems = file.iloc[:1,:].values[0][0]
    data = file.iloc[1:,:].values
    ret = []
    for idx, line in enumerate(data):
        if line[0].isdigit():
            problem_num = str(data[idx-1][0])
            threshold = int(line[0])
            items = HashTable()
            # items = []
            i = idx+1
            while len(data) > i and data[i][0].isdigit() == False:
                # chunks = re.split(' +', data[i][0])
                chunks = data[i][0].split('\t', 2)
                # chunks = data[i][0].split()
                if len(chunks) == 3:
                    # @ andrewpinkham why did you do it like this. why not a 2d array w item and (value, weight)
                    # items[chunks[0]] = (int(chunks[1]), int(chunks[2]))
                    items.put(chunks[0], (int(chunks[1]), int(chunks[2])))
                    # items.append([chunks[0], (chunks[1], chunks[2])])
                i+=1
            problem = Problem(_problem_num=problem_num, _threshold=threshold, _items=items)
            ret.append(problem)
    return ret


def solveKnapsackFile(file_name):
    problems = preprocess(file_name)
    # solver = Solver("BRUTE_FORCE")
    solver = Solver("DYNAMIC")
    # solver = Solver("BETTER_WAY")
    ret = []
    for problem in problems:
        # problem.prt()
        output = solver.solve(problem)
        ret.append(output)
    return ret

def format_results(result):
    # output = (list(map(lambda x:x[0], result)))
    result.sort(key=lambda x:x)
    return result
    # print(out)

def main():
    # results = solveKnapsackFile("toy_problems.txt")
    # results = solveKnapsackFile("problems_size20.txt")
    results = solveKnapsackFile("problems_size100.txt")
    # results = solveKnapsackFile("problems_size1000.txt")
    for idx, result in enumerate(results):
        print("---------------------------")
        print("Problem: {}".format(idx))
        print("Best Solution: {}".format(format_results(result)))
        # format_results(result)
        print("---------------------------")
        print(" ")

if __name__=="__main__":
    main()
