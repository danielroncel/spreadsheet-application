from abc import ABC,abstractmethod
from src.entities.FormulaContent import FormulaContent
from src.usecases.FormulaComputerVisitor import FormulaComputerVisitor
class Operand(FormulaContent, ABC):
    
    def __init__(self):
        pass
    
    @abstractmethod
    def get_value(self):
        pass
    
    @abstractmethod
    def set_value(self,content):
        pass

    @abstractmethod
    def accept_visitor(self, visitor:FormulaComputerVisitor):
        pass