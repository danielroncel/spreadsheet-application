import re
class Tokenizer:
    def __init__(self,formula:str):
        self.formula = formula

    def tokenize_expression(self):
        tokens = []
        pattern = re.compile(r'''
            (                   # Capturing group for each token type
                [+\-*/]          # Operator
                |[A-Za-z]+\d+    # Cell identifier
                |\d+             # Number
                |\(|\)           # Opening or closing round bracket
                |:               # Colon character
                |;               # Semi-colon character
                |,               # Comma
                |\w+             # Function name (assuming it consists of alphanumeric characters)
                |"[^"]*"         # Double-quoted string (e.g., function arguments)
                |[%&/|@#~$€¬'¡¿`^´_-]             # everything else
            )
        ''', re.VERBOSE)

        matches = pattern.findall(self.formula)

        for match in matches:
            tokens.append(match)

        return tokens
    

# Example usage:
formula = "=MEAN(SUM(A3:A17;B13;4),13$~''"
tokenizer = Tokenizer(formula)
tokens = tokenizer.tokenize_expression()
print(tokens)
