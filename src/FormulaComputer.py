from Tokenizer import Tokenizer
from CircularityChecker import CircularityChecker
from Parser import Parser
from PostfixEvaluator import PostfixEvaluator
from SpreadsheetMarkerForStudents.entities.circular_dependency_exception import CircularDependencyException
from UnexistingCellException import UnexistingCellException
from DependencyGraph import DependencyGraph

class FormulaComputer:

    def __init__(self, spreadsheet):
        self.spreadsheet = spreadsheet
        self.tokenizer = Tokenizer()
        self.circularityChecker = CircularityChecker(spreadsheet)
        self.postfixEvaluator = PostfixEvaluator(spreadsheet)
        self.parser = Parser()
        

    def compute_formula_value(self, formula: str, cellId: str) -> float:
        try: 
            tokens = self.tokenizer.tokenize_expression(formula)
            self.parser.parse_expression(tokens)
            expr = self.postfixEvaluator.generate_postfix_expression(tokens)
            dependent_cells = self.circularityChecker.get_referenced_cells(expr)   
            self.circularityChecker.check_circularities(cellId, dependent_cells)
            value = self.postfixEvaluator.evaluate_postfix_expression(expr)
            return [value, expr, dependent_cells]
        except Exception as ex:
            raise ex
        

class FormulaRecomputer:
    def __init__(self, spreadsheet):
        self.spreadsheet = spreadsheet
        self.postfixEvaluator = PostfixEvaluator(spreadsheet)

    def recompute_dependent_cell(self, cell_id):
        try: 
            to_recompute = set()
            cells = self.spreadsheet.get_cell(cell_id).get_depend_on_me()
            for el in cells:
                self.dfs(el, to_recompute)
            to_recompute = [self.spreadsheet.get_cell(el) for el in to_recompute]
            ordered = self.order_elements(to_recompute)
            
            for el in ordered:
                if el in to_recompute:
                    postfix = el.get_content().get_formula_content()
                    value = self.postfixEvaluator.evaluate_postfix_expression(postfix)
                    el.get_content().set_value(value)
        except Exception as ex: raise ex
    
    def dfs(self, el, to_recompute):
        if el not in to_recompute:
            to_recompute.add(el)
            try:
                dependents = self.spreadsheet.get_cell(el).get_depend_on_me()
                for cell_ref in dependents:
                    self.dfs(cell_ref, to_recompute)
            except Exception as ex: 
                raise ex
            
    def order_elements(self, to_update):
        """ 
        Implement a topological sort to find the optimal order for cell updating 
        
        """

        graph = DependencyGraph()

        for element in to_update:
            dependent = element
            dependencies = element.get_I_depend_on()
            for dependency in dependencies:
                graph.add_dependency(dependent, dependency)

        # Perform topological sort
        for element in to_update:
            if element not in graph.visited:
                graph.topological_sort(element)

        # Return the ordered set
        return reversed(graph.order)
        




        
        
        
        