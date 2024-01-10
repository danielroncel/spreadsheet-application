from src.entities.Function import Function
from src.usecases.FormulaComputerVisitor import FormulaComputerVisitor
class Max(Function):

    def __init__(self,arguments: []):
        super().__init__(arguments)
    
    
    def set_arguments(self,content):
        self.arguments = content

    def accept_visitor(self, visitor: FormulaComputerVisitor):
        visitor.visit_max_function(self)