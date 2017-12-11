#!/usr/bin/env python

import sys
import re
from AIGnode import AIGnode
from string import ascii_lowercase
from pprint import pprint


# usage: python aig_parser.py [filename]

fileName = sys.argv[1]
file = open(fileName, 'r')

# AIG header structure:
# token[0] => aag
# token[1] => M = maximum variable index
# token[2] => I = number of inputs
# token[3] => L = number of latches
# token[4] => O = number of outputs
# token[5] => A = number of AND gates
variables      = 0
inputs         = 0
latches        = 0
outputs        = 0
gates          = 0
aig            = {}
output_indexes = []

def get_node_expression(node):
    #print node
    if (node.isInput): #if is input
        return node.expr
    is_odd_in1 = node.in1 & 1
    is_odd_in2 = node.in2 & 1
    print("valor " + str(node.in1) + " eh impar " + str(is_odd_in1))
    print("valor " + str(node.in2) + " eh impar " + str(is_odd_in2))
    if (is_odd_in1 and is_odd_in2):
        return "!(" + get_node_expression(aig[node.in1-1]) + ")" + "*" + "!(" + get_node_expression(aig[node.in2-1]) + ")"

    elif (is_odd_in1 and not is_odd_in2):
        return "!(" + get_node_expression(aig[node.in1-1]) + ")" + "*" + get_node_expression(aig[node.in2])

    elif (not is_odd_in1 and is_odd_in2):
        return get_node_expression(aig[node.in1]) + "*" + "!(" + get_node_expression(aig[node.in2-1]) + ")"

    elif (not is_odd_in1 and not is_odd_in2):
        return get_node_expression(aig[node.in1]) + "*" + get_node_expression(aig[node.in2])

# PROGRAM BEGINS HERE
for i, line in enumerate(file):
    token = line.split(' ')
    # first pass, build dictionary from aig header
    if (i == 0):
        # print("header")
        variables   = int(token[1])
        inputs      = int(token[2])
        latches     = int(token[3])
        outputs     = int(token[4])
        gates       = int(token[5])

        # each variable can be either (+|-)
        keys = range(2, 2*(variables)+2,2) # starting at index 2 (thus, adding two more indexes in the range upper bound)
        aig  = dict.fromkeys(keys, AIGnode(False, False, "", -1, -1))

        # print "COMECOOO"
        # for key, value in aig.items() :
        #     print str(key) +": \n" + str(aig[key])
        # print "FIMMM"

    elif (i in range(1,1+inputs)):
        # handle inputs
        index_node        = int(token[0])
        node              = AIGnode(True, False, "v" + str(index_node), -1, -1)
        aig[index_node]   = node

        # not_node          = AIGnode(1,"(!v" + str(index_node) + ")", -1, -1)
        # aig[index_node+1] = not_node
        #print(not_node)

    elif (i in range(1+inputs,1+inputs+outputs)):
        # handle outputs
        index_node      = int(token[0])
        isInput_aux     = aig[index_node].isInput
        isExpr_aux      = aig[index_node].expr
        node            = AIGnode(isInput_aux, True, isExpr_aux, -1, -1)
        aig[index_node] = node

        output_indexes.append(index_node)

    elif (i in range(1+inputs+outputs,1+inputs+outputs+gates)):
        #handle ANDs

        index_node   = int(token[0])
        index_input1 = int(token[1])
        index_input2 = int(token[2])
        # print "index_input1: " + str(index_input1)
        # print "index_input2: " + str(index_input2)
        # print "INDEX: " + str(index_node)

        isInput_aux     = aig[index_node].isInput
        isOutput_aux    = aig[index_node].isOutput
        node            = AIGnode(isInput_aux, isOutput_aux, "", index_input1, index_input2)
        aig[index_node] = node

        # node = aig[index_node]
        # if node.isOutput:
        #     #if already set as output
        #     node = AIGnode(0,"", index_input1, index_input2)
        #     aig[index_node] = node #update aig
        # else:
        #     #not set as output
        #     node = AIGnode(2,"", index_input1, index_input2)
        #     aig[index_node] = node #update aig

        # print("ANDs")
        # print(line)

# print(keys)
# print(aig)
print "#:~:#| PRINT AIG |#:~:##:~:##:~:##:~:##:~:##:~:#\n"
for key, value in aig.items():
    print str(key) +": \n" + str(aig[key])
print "\n#:~:#| END AIG |#:~:##:~:##:~:##:~:##:~:##:~:#\n"


# sys.stdout.flush()
    #Here the AIG is stored in the 'aig' variable
for output_index in output_indexes:
    print "\n#:~:#| EXPRESSIONS |#:~:##:~:##:~:##:~:##:~:##:~:#\n"
    print "expression for node " + str(output_index)
    # print output_index
    # print aig[output_index]
    print get_node_expression(aig[output_index])

