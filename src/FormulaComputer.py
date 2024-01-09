from Tokenizer import Tokenizer
from CircularityChecker import CircularityChecker
from Parser import Parser
from PostfixEvaluator import PostfixEvaluator
from SpreadsheetMarkerForStudents.entities.circular_dependency_exception import CircularDependencyException
from UnexistingCellException import UnexistingCellException
from collections import defaultdict

class FormulaComputer:

    def __init__(self, spreadsheet):
        self.spreadsheet = spreadsheet
        self.tokenizer = Tokenizer()
        self.circularityChecker = CircularityChecker(self.spreadsheet)
        self.postfixEvaluator = PostfixEvaluator(self.spreadsheet)
        self.parser = Parser()
        

    def compute_formula_value(self, formula: str, cellId: str) -> float:
        
        try: 
            tokens = self.tokenizer.tokenize_expression(formula)
        except:
            raise SyntaxError("Tokenization error")
        
        try:
            self.parser.parse_expression(tokens)
        except:
            raise SyntaxError("Parsing error")
        try:   
            expr = self.postfixEvaluator.generate_postfix_expression(tokens)
        except:
            raise SyntaxError("Postfix generation error")
        try:
            dependent_cells = self.circularityChecker.get_referenced_cells(expr)   
            self.circularityChecker.check_circularities(cellId, dependent_cells)
        except CircularDependencyException:
            raise CircularDependencyException("Circularity detected")
        try:
            value = self.postfixEvaluator.evaluate_postfix_expression(expr)
            return [value, expr, dependent_cells]
        except:
            raise SyntaxError("Postfix evaluation error")
    
    def recompute_dependent_cell(self, cell_id):
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
                el.set_value(value)
    
    def dfs(self, el, to_recompute):
        to_recompute.add(el)
        try:
            dependents = self.spreadsheet.get_cell(el).get_depend_on_me()
            for cell_ref in dependents:
                self.dfs(cell_ref, to_recompute)
        except: 
            raise UnexistingCellException()
            
    def order_elements(self, to_update):
        graph = DependencyGraph()

        # Assuming each element in to_update has an 'i_depend_on' attribute
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
        

class DependencyGraph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.visited = set()
        self.order = []

    def add_dependency(self, dependent, dependency):
        self.graph[dependent].append(dependency)

    def topological_sort(self, node):
        self.visited.add(node)
        for dependency in self.graph[node]:
            if dependency not in self.visited:
                self.topological_sort(dependency)
        self.order.append(node)


        
        
        
        