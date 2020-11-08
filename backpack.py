#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 18:05:26 2020

@author: andrewpinkham
"""
import pandas as pd
import re

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
            items = {}
            i = idx+1
            while len(data) > i and data[i][0].isdigit() == False:
                # chunks = re.split(' +', data[i][0])
                chunks = data[i][0].split('\t', 2)
                if len(chunks) == 3:
                    items[chunks[0]] = (int(chunks[1]), int(chunks[2]))
                i+=1
            problem = Problem(_problem_num=problem_num, _threshold=threshold, _items=items)
            ret.append(problem)
    return ret


def solveKnapsackFile(file_name):
    problems = preprocess(file_name)
    solver = Solver("BRUTE_FORCE")
    # solver = Solver("BETTER_WAY")
    ret = []
    for problem in problems:
        # problem.prt()
        output = solver.solve(problem)
        ret.append(output)
    return ret

def main():
    # results = solveKnapsackFile("toy_problems.txt")
    results = solveKnapsackFile("problems_size20.txt")
    for idx, result in enumerate(results):
        print("---------------------------")
        print("Problem: {}".format(idx))
        print("Best Solution: {}".format(result))
        print("---------------------------")
        print(" ")

if __name__=="__main__":
    main()
