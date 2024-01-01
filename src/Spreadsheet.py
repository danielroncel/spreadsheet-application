import re

from Cell import Cell
from Content import Content
from CellComparator import CellComparator

from UnexistingCellException import UnexistingCellException

class Spreadsheet:
    
    def __init__(self):
        self.cells = dict()
        self.max_col = 'A'
        self.max_row = 1

    
    def create_cell(self, coord:str) -> Cell:
    
        if coord not in self.cells:
            self.cells[coord] = Cell(coord)
            
            match = re.match(r'([A-Z]+)(\d+)', coord)
            col, row = match.groups()
            
            if CellComparator.compare_columns(self.max_col, col) == 1:
                self.max_col = col
            if CellComparator.compare_rows(self.max_row, int(row)) == 1:
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


    def get_cell_type(self, coord:str):
        
        if coord in self.cells:
            return type(self.cells[coord].get_content())
        else:
            return None

    def get_cell_content(self, coord:str):
        
        if coord in self.cells:
            return self.cells[coord].get_content().get_value()
        else:
            return None
    

    def get_all_cell_coordinates(self) -> list:
        return list(self.cells.keys())
        