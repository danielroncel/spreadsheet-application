from Content import Content
from abc import abstractmethod
from FormulaContent import FormulaContent
####### REESCRIBIR. ESTO ES PARA TESTEAR SAVE

class Formula(Content):

    def __init__(self, str_content, value=None, formula_content: [FormulaContent] = None) -> None:
        self.content = str_content
        self.value = value
        self.formula_content = formula_content
        
        
    def get_content(self) -> str:
        return self.content
    
    def get_value(self) -> float:
        return self.value
    
    def set_value(self, value) -> None:
        self.value = value
    
    def set_content(self, content) -> None:
        self.content = content

    def get_formula_content(self) -> [FormulaContent]:
        return self.formula_content
    
    def set_formula_content(self, content: [FormulaContent]) -> None:
        self.formula_content = content
