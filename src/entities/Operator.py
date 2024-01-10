from src.entities.FormulaContent import FormulaContent
from src.usecases.FormulaComputerVisitor import FormulaComputerVisitor

class Operator(FormulaContent):
    
    def __init__(self,content:str) -> None:
        self.value = content
    
    def get_value(self):
        return self.value
    
    def set_value(self,content):
        self.value = content

    def accept_visitor(self, visitor:FormulaComputerVisitor):
        visitor.visit_operator(self)