from Cell import Cell
from Content import Content

from UnexistingCellException import UnexistingCellException

class Spreadsheet:
    
    def __init__(self):
        self.cells = dict()
    
    
    def create_cell(self, coord:str) -> Cell:
        if coord not in self.cells:
            self.cells[coord] = Cell(coord)
    
    
    def get_cell(self, coord:str) -> Cell:
        
        if coord in self.cells:
            return self.cells[coord]
        
        raise UnexistingCellException(f"There is no cell with coordinates {coord} in the spreadsheet")
        
    
    def add_content(self, coord:str, content:Content) -> None:
        cell = self.get_cell(coord)
        cell.set_content(content)


    def get_cell_content(self, coord:str):
        
        if coord in self.cells:
            return self.cells[coord].get_content().get_value()
        else:
            return None
    
    def get_all_cell_coordinates(self) -> list:
        return list(self.cells.keys())