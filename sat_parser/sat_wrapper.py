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
sats = [[],[]]
varNames = ["a", "a"]

def get_sat_expr_xor(in1, in2):
    A = in1
    B = in2
    Y = "ANS"
    return ("(" + "!" + Y + "+" + A + "+" + B + ")(" + Y + "+" + "!" + A + "+" + B + ")" + \
        "(" + Y + "+" + A + "+" + "!" + B + ")(" + "!" + Y + "+!" + A + "+!" + B + ")(" + Y + ")")

for i,aig in enumerate(aigs):
    p = Popen("python " "sat_parser.py" + " " + str(aig) + " " + str(varNames[i]), stdout = PIPE, stderr = PIPE, shell = True)
    stdout = p.communicate()[0].decode('utf-8').strip()
    for item in str(stdout).split("\n"):
        sats[i].append(str(item))


for sat0 in sats[0]:
    current_output_0 = sat0.split(" ")[0]
    current_sat_0 = sat0.split(" ")[1]
    
    for sat1 in sats[1]:
        current_output_1 = sat1.split(" ")[0]
        current_sat_1 = sat1.split(" ")[1]
        
        if (current_output_0 == current_output_1):
            print("calling xor for outputs from files " + str(aigs[0] + " and " + str(aigs[1] + ":")))
            print(current_sat_0)
            print(current_sat_1)
            print("xor: ")
            if ("s" in current_sat_0 and "s" in current_sat_1):
                xor = get_sat_expr_xor("s" + str(varNames[0]) + str(current_output_0), "s" + str(varNames[1]) + str(current_output_0))
            elif("s" in current_sat_0):
                xor = get_sat_expr_xor("s" + str(varNames[0]) + str(current_output_0), str(varNames[1]) + str(current_output_0))

            elif("s" in current_sat_1):
                xor = get_sat_expr_xor(str(varNames[0]) + str(current_output_0), "s" + str(varNames[1]) + str(current_output_0))
            else:
                xor = get_sat_expr_xor(str(varNames[0]) + str(current_output_0), str(varNames[1]) + str(current_output_0))

            print(current_sat_0 + current_sat_1 + xor)
        


