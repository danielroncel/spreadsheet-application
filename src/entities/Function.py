from abc import ABC, abstractmethod
from src.entities.Operand import Operand
from src.entities.Argument import Argument
from src.usecases.FormulaComputerVisitor import FormulaComputerVisitor

class Function(Operand, Argument, ABC):
    
    def __init__(self, arguments: []):
        self.arguments = arguments
        self.value = None

    def get_arguments(self):
        return self.arguments
    
    @abstractmethod
    def set_arguments(self,content):
        pass

    @abstractmethod
    def accept_visitor(self, visitor: FormulaComputerVisitor):
        pass

    
    def get_value(self):
        pass
    

    def set_value(self,content):
        pass

