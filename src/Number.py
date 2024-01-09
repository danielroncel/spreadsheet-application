from Operand import Operand
from Argument import Argument
from FormulaComputerVisitor import FormulaComputerVisitor
class Number(Operand, Argument):

    def __init__(self, num: float):
        self.value = num
    
    def get_value(self):
        return self.value
    
    def set_value(self,content):
        self.value = content

    def accept_visitor(self, visitor: FormulaComputerVisitor):
        visitor.visit_number(self)