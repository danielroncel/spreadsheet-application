from Operator import Operator
import numpy as np
from FormulaComputerVisitor import FormulaComputerVisitor
from Number import Number
from ReferenceToCell import ReferenceToCell,RangeOfCells
from Mean import Mean
from Sum import Sum
from Max import Max
from Min import Min
from FormulaContent import FormulaContent
import re

class PostfixEvaluator(FormulaComputerVisitor):
    def __init__(self, spreadsheet):
        self.stack = []
        self.priorities = {
            "(":0,
            ")":4,
            "+":1,
            "-":1,
            "*":2,
            "/":2,
            "%":2
        }
        self.spreadsheet = spreadsheet

    def generate_postfix_expression(self,infix_tokens):
            stack = []
            postfix_tokens = []

            end = len(infix_tokens)
            i=0
            while i<end:
                token = infix_tokens[i]
                if token.isdigit():
                    postfix_tokens.append(Number(float(token)))
                    i+=1
                elif self.is_cell_reference(token):
                    postfix_tokens.append(ReferenceToCell(token))
                    i+=1
                elif token == '(':
                    stack.append(token)
                    i+=1
                elif token == ')':
                    while stack and stack[-1] != '(':
                        postfix_tokens.append(Operator(stack.pop()))
                    stack.pop()  # Pop '(' from the stack
                    i+=1
                elif self.is_function(token):
                    count, in_brackets = self.find_matching_parenthesis(infix_tokens[i+1:])
                    i += (count+1)
                    val = self.generate_function_content(in_brackets, token)
                    postfix_tokens.append(val)
                else:
                    while stack and self.priorities[stack[-1]] >= self.priorities[token]:
                        postfix_tokens.append(Operator(stack.pop()))
                    stack.append(token)
                    i+=1

            while stack:
                postfix_tokens.append(Operator(stack.pop()))

            return postfix_tokens 
    
    def is_cell_reference(self, token):
        cell_ref = re.compile(r'''([A-Za-z]+\d+)''', re.VERBOSE)
        return cell_ref.search(token) != None
    
    def is_function(self, token):
        functions = re.compile(r'''
            (                   # Capturing group for each token type
                sum|SUMA|Sum|SUM             # Function name (assuming it consists of these combinations)
                |mean|MEAN|Mean|PROMEDIO
                |min| MIN | Min
                |max|MAX|Max
            )
        ''', re.VERBOSE)
        return functions.search(token) != None
    
    def find_matching_parenthesis(self,tokens):
        # Find the matching closing parenthesis
        if len(tokens) <= 2:
            raise SyntaxError("Parsing error. Empty function")
        count = 1
        i = 1
        end = len(tokens)
        in_brackets = []
        if tokens[i] == ')':
            raise SyntaxError("Empty parenthesis")
        while i < end and count > 0:
            if tokens[i] == '(':
                count += 1
            elif tokens[i] == ')':
                count -= 1
            in_brackets.append(tokens[i])
            i += 1
            
        if count > 0:
            raise SyntaxError("Unbalanced parenthesis")
        
        return [i,in_brackets[:-1]]
    
    def generate_function_content(self, tokens, tok):
        args = []
        i = 0
        end = len(tokens)

        while i < end: 
            token = tokens[i]
            if token.isdigit():
                val = Number(float(token))
                args.append(val)
                i += 1
            elif self.is_cell_reference(token):
                if i < end-2 and tokens[i+1] == ':':
                    val = RangeOfCells(token, tokens[i+2])
                    cell_ids = val.get_value()
                    for id in cell_ids:
                        args.append(ReferenceToCell(id))
                    i+=3
                else:
                    val =ReferenceToCell(token)
                    i+=2
                    args.append(val)
            elif self.is_function(token):
                i +=1
                count, in_brackets = self.find_matching_parenthesis(tokens[i:])
                i += count
                val = self.generate_function_content(in_brackets, token)
                args.append(val)
            else: 
                i+=1
        if tok == 'sum'or tok =='SUMA'or tok =='Sum' or tok =='SUM': content = Sum(args)
        elif tok == 'Mean'or tok =='mean'or tok =='MEAN' or tok =='PROMEDIO': content = Mean(args)
        elif tok == 'min'or tok =='MIN'or tok =='Min': content = Min(args)
        elif tok == 'max'or tok =='MAX'or tok =='Max': content = Max(args)
        return content
    
    
    def evaluate_postfix_expression(self, postfix: FormulaContent): 
        self.stack = []
        for el in postfix:
            el.accept_visitor(self)
        return self.stack.pop()

    def visit_operator(self, op: Operator):
        sec_op = self.stack.pop()
        first_op = self.stack.pop()
        res = eval(str(first_op) + op.get_value() + str(sec_op))
        self.stack.append(res)

    def visit_number(self, num: Number):
        self.stack.append(num.get_value())

    def visit_cell_reference(self, ref: ReferenceToCell):
        cell_id = ref.get_value()
        try:
            val = self.spreadsheet.get_cell(cell_id).get_content().get_value()
            self.stack.append(val)
        except: print("Unexisting cell expection")

    def visit_mean_function(self, fun: Mean):
        args = fun.get_arguments()
        arg_values = []
        for arg in args:
            arg.accept_visitor(self)
            arg_values.append(self.stack.pop())
        self.stack.append(np.mean(arg_values))
    
    def visit_min_function(self, fun: Min):
        args = fun.get_arguments()
        arg_values = []
        for arg in args:
            arg.accept_visitor(self)
            arg_values.append(self.stack.pop())
        self.stack.append(min(arg_values))

    def visit_max_function(self, fun: Max):
        args = fun.get_arguments()
        arg_values = []
        for arg in args:
            arg.accept_visitor(self)
            arg_values.append(self.stack.pop())
        self.stack.append(max(arg_values))

    def visit_sum_function(self, fun: Sum):
        args = fun.get_arguments()
        arg_values = []
        for arg in args:
            arg.accept_visitor(self)
            arg_values.append(self.stack.pop())
        val = sum(arg_values)
        self.stack.append(val)


    def visit_range_of_cells(self,range:RangeOfCells):
        cell_ids = range.get_value()
        for cell_id in cell_ids:
            try:
                val = self.spreadsheet.get_cell(cell_id).get_content().get_value()
                self.stack.append(val)
            except: print("Unexisting cell")

