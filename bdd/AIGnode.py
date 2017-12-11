#!/usr/bin/env python

import sys
import re
from string import ascii_lowercase

class AIGnode:
    isInput  = False
    isOutput = False
    expr     = ""
    in1      = -1
    in2      = -1

    # def __init__(self):
    #     type = -1
    #     expr = ""
    #     in1  = -1
    #     in2  = -1

    # def __init__(self, type, expr):
    #     self.type = type
    #     self.expr = expr

    def __init__(self, isInput, isOutput, expr, in1, in2):
        self.isInput  = isInput
        self.isOutput = isOutput
        self.expr     = expr
        self.in1      = in1
        self.in2      = in2

    def __str__(self):
        return ("isInput: %s \nisOutput: %s \nexpr: %s \nin1: %s \nin2: %s\n\n" % (self.isInput, self.isOutput, self.expr, self.in1, self.in2))

    def set_as_output(self, isOutput):
        self.isOutput = isOutput

    def set_from_inputs(self, in1, in2):
        self.in1 = in1
        self.in2 = in2

    def get_object(self):
        return self