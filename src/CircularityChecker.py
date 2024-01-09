from FormulaContent import FormulaContent
from ReferenceToCell import ReferenceToCell
from Function import Function
from UnexistingCellException import UnexistingCellException
from SpreadsheetMarkerForStudents.entities.circular_dependency_exception import CircularDependencyException

class CircularityChecker:
    def __init__(self, spreadsheet):
        self.spreadsheet = spreadsheet
        self.visited = set()


    def check_circularities(self, cellId,cell_references):
        self.visited.add(cellId)
        for el in cell_references:
            self.dfs(el, cellId)
        

    def dfs(self, el, cell_id):
        id = el
        if id == cell_id:
            raise CircularDependencyException("Circularity detected")
        if id not in self.visited:
            self.visited.add(id)
            try:
                dependents = self.spreadsheet.get_cell(id).get_I_depend_on()
                for cell_ref in dependents:
                    self.dfs(cell_ref, cell_id)
            except: 
                raise UnexistingCellException()

    def get_referenced_cells(self, postfix_tokens:FormulaContent) ->[ReferenceToCell]:
        ref_cells = []
        for els in postfix_tokens:
            if type(els) == ReferenceToCell: 
                ref_cells.append(els.get_value())
            elif type(els) == Function:
                ref_func_cells = self.get_referenced_cells(els.get_arguments())
                for e in ref_func_cells:
                    ref_cells.append(e) 
        return ref_cells