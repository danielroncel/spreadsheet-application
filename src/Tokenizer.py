import re
from SpreadsheetMarkerForStudents.entities.content_exception import ContentException
from FormulaSyntaxException import FormulaSyntaxException

class Tokenizer:
    def __init__(self):
        self.pattern = re.compile(r'''
            (                   # Capturing group for each token type
                [+\-*/]          # Operator
                |[A-Za-z]+\d+    # Cell identifier
                |\d+             # Number
                |\(|\)           # Opening or closing round bracket
                |:               # Colon character
                |;               # Semi-colon character
                |,               # Comma
                |sum|SUMA|Sum|SUM             # Function name (assuming it consists of these combinations)
                |mean|MEAN|Mean|PROMEDIO
                |min| MIN | Min
                |max|MAX|Max
            )
        ''', re.VERBOSE)


    def tokenize_expression(self, formula:str) -> [str]:
        tokens = []

        matches = self.pattern.split(formula)

        if matches[0]== '' or matches[1]== '':
            raise FormulaSyntaxException(f"Syntactical error in formula spelling")

        for i in range(1, len(matches)-1, 2):
        # Check if the entry is not an empty string
            if matches[i+1] != '':
                raise FormulaSyntaxException(f"Syntactical error in formula spelling")
            else:
                tokens.append(matches[i])

        return tokens
    
