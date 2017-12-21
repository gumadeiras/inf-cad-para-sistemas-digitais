#!/usr/bin/env python

import os
import sys
import re
import subprocess
from subprocess import Popen, PIPE
from AIGnode import AIGnode
from string import ascii_lowercase
from pprint import pprint


# usage: python wrapper.py [aig1] [aig2]

aigs = [sys.argv[1], sys.argv[2]]
expressions = [[],[]]

for i,aig in enumerate(aigs):
    p = Popen("python " "aig_parser.py" + " " + str(aig), stdout = PIPE, stderr = PIPE, shell = True)
    stdout = p.communicate()[0].decode('utf-8').strip()
    for item in str(stdout).split("\n"):
        expressions[i].append(str(item))


for expr0 in expressions[0]:
    current_output_0 = expr0.split(" ")[0]
    current_expr_0 = expr0.split(" ")[1]
    
    for expr1 in expressions[1]:
        current_output_1 = expr1.split(" ")[0]
        current_expr_1 = expr1.split(" ")[1]
        
        if (current_output_0 == current_output_1):
            print("calling bdd for output " + str(current_output_0) + " from files " + str(aigs[0] + " and " + str(aigs[1] + ":")))
            print(current_expr_0)
            print(current_expr_1)
            
        
p = Popen("./evalBDD " + "'" + str(current_expr_0) + "' '" + str(current_expr_1) + "'", stdout = PIPE, stderr = PIPE, shell = True)
stdout = p.communicate()[0].decode('utf-8').strip()
print(stdout)