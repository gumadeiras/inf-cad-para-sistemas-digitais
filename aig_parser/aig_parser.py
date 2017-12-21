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

def is_odd(value):
	return ( (value & 1) == 1)

def is_even(value):
	return ( (value & 1) == 0)

def get_node_expression(node):
    #print node
    if (node.isInput): #if is input
        return node.expr

    if (is_odd(node.in1) and is_odd(node.in2)):
        return "!(" + get_node_expression(aig[node.in1-1]) + ")" + "*" + "!(" + get_node_expression(aig[node.in2-1]) + ")"

    elif (is_odd(node.in1) and is_even(node.in2)):
        return "!(" + get_node_expression(aig[node.in1-1]) + ")" + "*" + get_node_expression(aig[node.in2])

    elif (is_even(node.in1) and is_odd(node.in2)):
        return get_node_expression(aig[node.in1]) + "*" + "!(" + get_node_expression(aig[node.in2-1]) + ")"

    elif (is_even(node.in1) and is_even(node.in2)):
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
        if is_even(index_node):
        	isInput_aux     = aig[index_node].isInput
        	expr_aux      	= aig[index_node].expr
        else:
        	isInput_aux     = aig[index_node-1].isInput # inputs are always referenced by even numbers
        	expr_aux      	= aig[index_node-1].expr
        node            = AIGnode(isInput_aux, True, expr_aux, -1, -1)
        aig[index_node] = node

        output_indexes.append(index_node)

    elif (i in range(1+inputs+outputs,1+inputs+outputs+gates)):
        #handle ANDs

        index_node   = int(token[0])
        index_input1 = int(token[1])
        index_input2 = int(token[2])

        isInput_aux     = aig[index_node].isInput
        isOutput_aux    = aig[index_node].isOutput
        node            = AIGnode(isInput_aux, isOutput_aux, "", index_input1, index_input2)
        aig[index_node] = node

for output_index in output_indexes:
    if is_even(output_index):
        print str( str(output_index) + " " + get_node_expression(aig[output_index]) )
    else:
        print str( str(output_index-1) + " " + "!(" + get_node_expression(aig[output_index-1]) + ")" )
