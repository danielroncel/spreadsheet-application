from FormulaContent import FormulaContent
from ReferenceToCell import ReferenceToCell
from Function import Function
from SpreadsheetMarkerForStudents.entities.circular_dependency_exception import CircularDependencyException

class CircularityChecker:
    def __init__(self, spreadsheet):
        self.spreadsheet = spreadsheet
        self.visited = set()


    def check_circularities(self, cellId,cell_references):
        self.visited = set()
        self.visited.add(cellId)
        for el in cell_references:
            self.dfs(el, cellId)
        

    def dfs(self, el, cell_id):
        id = el
        if id == cell_id:
            raise CircularDependencyException(f"Circularity detected in cell {cell_id}")
        if id not in self.visited:
            self.visited.add(id)
            cell = self.spreadsheet.get_cell(id)
            dependents = cell.get_I_depend_on()
            try:
                for cell_ref in dependents:
                    self.dfs(cell_ref, cell_id)
            except CircularDependencyException as ex: raise ex

    def get_referenced_cells(self, postfix_tokens:FormulaContent) ->[ReferenceToCell]:
        ref_cells = set()
        for els in postfix_tokens:
            if type(els) == ReferenceToCell: 
                ref_cells.add(els.get_value())
            elif isinstance(els, Function):
                ref_func_cells = self.get_referenced_cells(els.get_arguments())
                for e in ref_func_cells:
                    ref_cells.add(e)
        return ref_cells