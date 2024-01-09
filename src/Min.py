from Function import Function
from FormulaComputerVisitor import FormulaComputerVisitor

class Min(Function):

    def __init__(self, arguments):
        super().__init__(arguments)

    def set_arguments(self,content):
        self.arguments = content

    def accept_visitor(self, visitor: FormulaComputerVisitor):
        visitor.visit_min_function(self)
