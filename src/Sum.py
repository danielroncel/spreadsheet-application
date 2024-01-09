from Function import Function
from FormulaComputerVisitor import FormulaComputerVisitor

class Sum(Function):

    def __init__(self, arguments):
        super().__init__(arguments)

    def set_arguments(self,content):
        self.arguments = content

    def accept_visitor(self, visitor: FormulaComputerVisitor):
        visitor.visit_sum_function(self)
