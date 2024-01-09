from abc import ABC, abstractmethod

class FormulaComputerVisitor(ABC):
    def __init__(self) ->None:
        pass
    
    @abstractmethod
    def visit_operator(self, op):
        pass

    @abstractmethod
    def visit_number(self, num):
        pass

    @abstractmethod
    def visit_cell_reference(self, ref):
        pass


    @abstractmethod
    def visit_range_of_cells(self,range):
        pass

    @abstractmethod
    def visit_min_function(self, min_func):
        pass

    @abstractmethod
    def visit_max_function(self, min_func):
        pass

    @abstractmethod
    def visit_mean_function(self, min_func):
        pass

    @abstractmethod
    def visit_sum_function(self, min_func):
        pass
