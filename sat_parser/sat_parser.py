#!/usr/bin/env python

import sys
import re
from SATnode import AIGnode
from string import ascii_lowercase
from pprint import pprint
import re

# usage: python aig_parser.py [filename]

fileName = sys.argv[1]
varName  = sys.argv[2]
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

# both inputs are negative
def get_sat_expr_nn(in1, in2, out):
    A = "v" + str(in1 - 1)
    B = "v" + str(in2 - 1)
    Y = str(varName) + str(out)
    return ("(" + "!" + Y + "+" + "!" + A + ")(" + "!" + Y + "+" + "!" + B + ")(" + Y + "+" + A + "+" + B + ")")

# both inputs are positive
def get_sat_expr_pp(in1, in2, out):
    A = "v" + str(in1)
    B = "v" + str(in2)
    Y = str(varName) + str(out)
    return ("(" + "!" + Y + "+" + A + ")(" + "!" + Y + "+" + B + ")(" + Y + "+" + "!" + A + "+" + "!" + B + ")")

def get_sat_expr_pn(in1, in2, out):
    A = "v" + str(in1)
    B = "v" + str(in2 - 1)
    Y = str(varName) + str(out)
    return ("(" + "!" + Y + "+" + A + ")(" + "!" + Y + "+" + "!" + B + ")(" + Y + "+" + "!" + A + "+" + B + ")")

def get_sat_expr_np(in1, in2, out):
    A = "v" + str(in1 - 1)
    B = "v" + str(in2)
    Y = str(varName) + str(out)
    return ("(" + "!" + Y + "+" + "!" + A + ")(" + "!" + Y + "+" + B + ")(" + Y + "+" + A + "+" + "!" + B + ")")


def get_sat_expression(node):
    # print node

    if (aig[node.in1].isInput if (is_even(node.in1)) else aig[node.in1-1].isInput ): # if input of the node is a leaf

        if (is_odd(node.in1) and is_odd(node.in2)):
            return get_sat_expr_nn(node.in1, node.in2, node.index)

        elif (is_odd(node.in1) and is_even(node.in2)):
            return get_sat_expr_np(node.in1, node.in2, node.index)

        elif (is_even(node.in1) and is_odd(node.in2)):
            return get_sat_expr_pn(node.in1, node.in2, node.index)

        elif (is_even(node.in1) and is_even(node.in2)):
            return get_sat_expr_pp(node.in1, node.in2, node.index)


    if (is_odd(node.in1) and is_odd(node.in2)):
        return get_sat_expression(aig[node.in1-1]) + get_sat_expression(aig[node.in2-1]) + get_sat_expr_nn(node.in1, node.in2, node.index)

    elif (is_odd(node.in1) and is_even(node.in2)):
        return get_sat_expression(aig[node.in1-1]) + get_sat_expression(aig[node.in2]) + get_sat_expr_np(node.in1, node.in2, node.index)

    elif (is_even(node.in1) and is_odd(node.in2)):
        return get_sat_expression(aig[node.in1]) + get_sat_expression(aig[node.in2-1]) + get_sat_expr_pn(node.in1, node.in2, node.index)

    elif (is_even(node.in1) and is_even(node.in2)):
        return get_sat_expression(aig[node.in1]) + get_sat_expression(aig[node.in2]) + get_sat_expr_pp(node.in1, node.in2, node.index)

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
        aig  = dict.fromkeys(keys, AIGnode(False, False, -1, -1, -1))

    elif (i in range(1,1+inputs)):
        # handle inputs
        index_node        = int(token[0])
        node              = AIGnode(True, False, index_node, -1, -1)
        aig[index_node]   = node

    elif (i in range(1+inputs,1+inputs+outputs)):
        # handle outputs
        index_node      = int(token[0])
        if is_even(index_node):
            isInput_aux     = aig[index_node].isInput
        else:
            isInput_aux     = aig[index_node-1].isInput #inputs sempre sao referenciadas pelos numeros pares
            
        node            = AIGnode(isInput_aux, True, index_node, -1, -1)
        aig[index_node] = node

        output_indexes.append(index_node)

    elif (i in range(1+inputs+outputs,1+inputs+outputs+gates)):
        #handle ANDs

        index_node   = int(token[0])
        index_input1 = int(token[1])
        index_input2 = int(token[2])
        isInput_aux     = aig[index_node].isInput
        isOutput_aux    = aig[index_node].isOutput
        node            = AIGnode(isInput_aux, isOutput_aux, index_node, index_input1, index_input2)
        aig[index_node] = node

    #Here the AIG is stored in the 'aig' variable
for output_index in output_indexes:

    if is_even(output_index):
        print str(str(output_index) + " " + get_sat_expression(aig[output_index]) )
    else:
        print str(str(output_index-1) + " " + get_sat_expression(aig[output_index-1]) \
            + "(" + "s" + str(varName) + str(output_index-1) + "+" + str(varName) + str(output_index-1) + ")" + "(" + "!s" + str(varName) + str(output_index-1) \
            + "+" + "!" + str(varName) + str(output_index-1) + ")")