#!/usr/bin/env python

import sys
import re
from string import ascii_lowercase

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
header    = 0
variables = 0
inputs    = 0
latches   = 0
outputs   = 0
gates     = 0
table     = {}

# iterate lines in file
for line in file:
    token = line.split(' ')

    # first pass, build dictionary from aig header
    if (header == 0):
        header      = 1
        variables   = int(token[1])
        inputs      = int(token[2])
        latches     = int(token[3])
        outputs     = int(token[4])
        gates       = int(token[5])

        # each variable can be either (+|-)
        keys = range(2,2*(variables)+2) #starting at index 2 (thus, adding two more indexes in the range upper bound)
        table = dict.fromkeys(keys)
    
        # for key in table:
        # for c in ascii_lowercase:
        # iterar no dict e atribuir uma letra pra cada variavel

print(keys)
print(table)