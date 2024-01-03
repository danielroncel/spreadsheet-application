from abc import ABC, abstractmethod
from Spreadsheet import Spreadsheet 
from Tokenizer imporrt Tokenizer
from CircularityChecker import CircularityChecker
from Parser import Parser
from PostfixEvaluator import PostfixEvaluator

class FormulaComputer:

    def __init__(self, spreadsheet, formula: str, cell: Cell):
        self.spreadsheet = spreadsheet
        self.formula = formula
        self.cell = cell

    def compute_formula_value(self) -> float:
        tokens = Tokenizer.tokenize(formula)
        try: 
            circularityChecker = CircularityChecker(self.cell.getId(), self.spreadsheet, tokens)
            circularityChecker.check_circularities()
        except:
            #change to output through controller u/i
            print("Circularity detected. Unable to assign formula to cell")
        
        tokens = PostfixEvaluator.reorder_tokens(Parser.parse_expression(tokens))
        return PostfixEvaluator.evaluate_postfix_expression(PostfixEvaluator.generate_postfix_expression(tokens))