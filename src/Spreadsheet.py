import re

from Cell import Cell
from Content import Content
from CellComparator import CellComparator
from FormulaComputer import FormulaComputer
from UnexistingCellException import UnexistingCellException
from CellPrechecker import CellPrechecker
from CellFactory import CellFactory
from FormulaContent import FormulaContent
from CircularityChecker import CircularityChecker

class Spreadsheet:
    
    def __init__(self):
        self.cells = dict()
        self.max_col = 'A'
        self.max_row = 1
        self.formula_computer = FormulaComputer(self)
        self.cell_comparator = CellComparator()
        self.cell_prechecker = CellPrechecker()
        self.cell_factory = CellFactory()
        self.circularity_checker = CircularityChecker(self)
    
    def create_cell(self, coord:str) -> Cell:
    
        if coord not in self.cells:
            self.cells[coord] = Cell(coord)
            
            match = re.match(r'([A-Z]+)(\d+)', coord)
            col, row = match.groups()
            
            if self.cell_comparator.compare_columns(self.max_col, col) == 1:
                self.max_col = col
            if self.cell_comparator.compare_rows(self.max_row, int(row)) == 1:
                self.max_row = int(row)
        
            
    def get_max_row(self) -> int:
        return self.max_row
    
    
    def get_max_col(self) -> str:
        return self.max_col
    
    
    def get_cell(self, coord:str) -> Cell:
        
        if coord in self.cells:
            return self.cells[coord]
        
        raise UnexistingCellException(f"There is no cell with coordinates {coord} in the spreadsheet")
        
    
    def add_content(self, coord:str, content:Content) -> None:
        cell = self.get_cell(coord)
        cell.set_content(content)

    def add_value(self, coord:str, value) -> None:
        cell = self.get_cell(coord)
        cell.set_value(value)

    def compute_formula_value(self, str_content, coord):
        return self.formula_computer.compute_formula_value(str_content,coord)
    
    
    def get_cell_type(self, coord:str):
        
        if coord in self.cells:
            return type(self.cells[coord].get_content())
        else:
            return None

    def get_cell_content(self, coord:str):
        
        if coord in self.cells:
            return self.cells[coord].get_value()
        else:
            return None
    

    def get_all_cell_coordinates(self) -> list:
        return list(self.cells.keys())
    
    def check_for_circularities(self, expr: FormulaContent, cell_id):
        dependent_cells = self.circularity_checker.get_referenced_cells(expr)   
        self.circularity_checker.check_circularities(cell_id, dependent_cells)

    def update_dependencies(self, dependent,cell_id):
        for s in  dependent:
            arr = self.get_cell(s).get_depend_on_me()
            arr.add(cell_id)
            self.get_cell(s).set_depend_on_me(arr)

    def recompute_dependent_cells(self,cell_id):
        self.formula_computer.recompute_dependent_cell(cell_id)