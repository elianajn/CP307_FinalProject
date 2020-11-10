#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 18:05:26 2020

@author: andrewpinkham
"""
import pandas as pd
import re
import heapq
import numpy as np

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
        elif self.method == "BETTER_WAY":
            return self.better_way(problem)
        elif self.method == "BRANCH_AND_BOUND":
            return self.branchandbound(problem)
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

    def better_way(self, problem):
        #our better way!
        return "to-do"

    def sub_lists(self, l):
        base = []
        lists = [base]
        for i in range(len(l)):
            orig = lists[:]
            new = l[i]
            for j in range(len(lists)):
                lists[j] = lists[j] + [new]
            lists = orig + lists
        return lists

    def branchandbound(self, problem):
        scoredItems = self.scoreItems(problem)
        heap = []
        # for item in scoredItems:
        #     heapq.heappush(li,4)
        return []

    # scores items value - weight
    # returns list of tuples (item name, score)
    def scoreItems(self, problem):
        scoredItems = []
        for item in problem.items:
            valueStr, weightStr = item[1]
            value = int(valueStr)
            weight = int(weightStr)
            score = value - weight
            scoredItems.append((item[0], -score)) # returning as inverted bc there is only minheap
        return scoredItems

    def dynamic(self, problem):
        # matrix = []
        width = int(problem.threshold) + 1
        height = len(problem.items)
        matrix = np.zeros((height, width))
        # sortedItems is a list of tuples (weight,item)
        sortedItems = self.sortItems(problem)
        # number of columns is the total weight
        # number of rows is the number of items
        for row in range(len(problem.items)):
            for col in range(width):
                item, (valueS, weightS) = sortedItems[row]
                # print(item)
                # value = int(item[0])
                value = int(valueS)
                # weight = int(item[1])
                weight = int(weightS)
                # matrix.append([])
                # print(matrix)
                if row == 0:
                    # print("weight at 0: ", weight)
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
            if r != 0 and matrix[r][c] == matrix[r-1][c]:
                continue
            if r != 0 and matrix[r][c] != matrix[r-1][c]:
                item = sortedItems[r]
                selected_items.append(item)
                weight = item[1][1]
                c -= int(weight)
                if c < 0:
                    break
            elif r == 0:
                item = sortedItems[r]
                weight = int(item[1][1])
                if weight <= c:
                    selected_items.append(item)
        return selected_items


    def sortItems(self, problem):
        output = []
        c = 0
        ls = (problem.items)
        # weight = 0
        for item in problem.items:
            weight = int(item[1][1])
            output.append([])
            # output.append((weight, item))
            output[c].append(weight)
            output[c].append(item)
            c += 1
        output.sort(key=lambda x:x[0])
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
            # items = {}
            items = []
            i = idx+1
            while len(data) > i and data[i][0].isdigit() == False:
                # chunks = re.split(' +', data[i][0])
                # chunks = data[i][0].split('\t', 2)
                chunks = data[i][0].split()
                if len(chunks) == 3:
                    # @ andrewpinkham why did you do it like this. why not a 2d array w item and (value, weight)
                    # items[chunks[0]] = (int(chunks[1]), int(chunks[2]))
                    items.append([chunks[0], (chunks[1], chunks[2])])
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
    output = (list(map(lambda x:x[0], result)))
    output.sort(key=lambda x:x[0])
    return output
    # print(out)

def main():
    # results = solveKnapsackFile("toy_problems.txt")
    results = solveKnapsackFile("problems_size20.txt")
    for idx, result in enumerate(results):
        print("---------------------------")
        print("Problem: {}".format(idx))
        print("Best Solution: {}".format(format_results(result)))
        # format_results(result)
        print("---------------------------")
        print(" ")

if __name__=="__main__":
    main()
