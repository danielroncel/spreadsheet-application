from abc import ABC, abstractmethod
from FormulaComputerVisitor import FormulaComputerVisitor

class FormulaContent(ABC):

    @abstractmethod
    def get_value(self):
        pass
    
    @abstractmethod
    def set_value(self,formula_content):
        pass

    @abstractmethod
    def accept_visitor(self, visitor: FormulaComputerVisitor):
        pass