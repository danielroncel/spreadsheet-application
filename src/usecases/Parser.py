"""
Syntactic rules of an arithmethic expression: 
    - Must be balanced (equal number or opening and closing brackets)
    - +,-,x,/ can only be placed between numbers, after a number, after a closing parenthesis, after a reference to cell,
      before opening perenthesis, before reference to cell. NEVER inside a function, right after opening parenthesis or before or 
      after ";", ":", or other operators.
    - ; must always be present between numbers and or referenceToCells 
    - : must always be present between reterenceToCells 
    - A function name must always be followed by an opening parenthesis
"""
import re
from src.exceptions.ParsingException import ParsingException

class Parser:
    def __init__(self):
        self.operators = {'+', '-', '*', '/'}
        self.functions = re.compile(r'''
            (                   # Capturing group for each token type
                sum|SUMA|Sum|SUM           # Function name (assuming it consists of these combinations)
                |mean|MEAN|Mean|PROMEDIO
                |min| MIN | Min
                |max|MAX|Max
            )
        ''', re.VERBOSE)
    
   
    def parse_expression(self, tokens):
        
        i = 0
        end = len(tokens)
        while i < end:
            token = tokens[i]

            if token.isdigit():
                self.validate_operator_presence(i, end, tokens)
                i += 2
            elif self.is_cell_reference(token):
                self.validate_operator_presence(i, end, tokens)
                i += 2
            elif token in self.operators:
                if i==0 or i==end-1 or (i>0 and tokens[i-1] != ')'):
                    raise ParsingException(f"Unexpected operator '{token}' at position {i}")
                i+=1
            elif token == '(':
                count, in_brackets = self.find_matching_parenthesis(tokens[i:])
                i += count
                self.parse_expression(in_brackets)
            elif token == ')':
                raise ParsingException("Unbalanced parenthesis")
            elif self.functions.search(token) != None:
                i +=1
                count, in_brackets = self.find_matching_parenthesis(tokens[i:])
                i += count
                self.parse_function(in_brackets)
        
            else:
                raise ParsingException(f"Unexpected token: {token}")


    def is_cell_reference(self, token):
        cell_ref = re.compile(r'''([A-Za-z]+\d+)''', re.VERBOSE)
        return cell_ref.search(token) != None

    def validate_operator_presence(self, i, end, tokens):
        # Check if there is an operator between two numbers or cell references
        if i < end - 1 and tokens[i+1] not in self.operators:
            raise ParsingException(f"Parsing error")

    def parse_function(self,tokens):
        i = 0
        end = len(tokens)

        while i < end: 
            token = tokens[i]

            if token.isdigit():
                i += 1
                if i < end and tokens[i] != ';':
                    raise ParsingException(f"Parsing error inside function")
                i += 1
            elif self.is_cell_reference(token):
                i += 1
                if i < end and tokens[i] == ';':
                    i+=1
                elif i < end and tokens[i] == ':':
                    i += 1 
                    if i < end and not self.is_cell_reference(tokens[i]):
                        raise ParsingException(f"Parsing error inside function")
                    i += 1
                    if i < end and not tokens[i] == ';':
                        raise ParsingException(f"Parsing error inside function")
                    i+=1
            elif self.functions.search(token) != None:
                i +=1
                if i == end: 
                    raise ParsingException(f"Parsing error inside function")
                count, in_brackets = self.find_matching_parenthesis(tokens[i:])
                i += count
                self.parse_function(in_brackets)
                if i < end and tokens[i] != ';':
                    raise ParsingException(f"Parsing error inside function")
            else: 
                raise ParsingException(f"Parsing error inside function")

    def find_matching_parenthesis(self,tokens):
        # Find the matching closing parenthesis
        if len(tokens) <= 2:
            raise ParsingException("Parsing error. Empty function")
        count = 1
        i = 1
        end = len(tokens)
        in_brackets = []
        if tokens[i] == ')':
            raise ParsingException("Empty parenthesis")
        while i < end and count > 0:
            if tokens[i] == '(':
                count += 1
            elif tokens[i] == ')':
                count -= 1
            in_brackets.append(tokens[i])
            i += 1
            
        if count > 0:
            raise ParsingException("Unbalanced parenthesis")
        
        return [i,in_brackets[:-1]]