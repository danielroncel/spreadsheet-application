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
        
        """If it does not exists, create a cell in the spreadsheet with the
        specified coordinates.
        
        Arguments:
            coord -- string representing the coordinates of a cell
        """
        
        # Only create it if it does not exist
        if coord not in self.cells:
            self.cells[coord] = Cell(coord)
            
            # Extract the column and the row
            match = re.match(r'([A-Z]+)(\d+)', coord)
            col, row = match.groups()
            
            # Update which is the column more distance of 'A' column with
            # a created cell
            if CellComparator.compare_columns(self.max_col, col) == 1:
                self.max_col = col
            # Update which is the row more distance of 'A' column with
            # a created cell
            if CellComparator.compare_rows(self.max_row, int(row)) == 1:
                self.max_row = int(row)
        
            
    def get_max_row(self) -> int:
        return self.max_row
    
    
    def get_max_col(self) -> str:
        return self.max_col
    
    
    def get_cell(self, coord:str) -> Cell:
        
        """Try to return the cell at the specified coordinates

        Arguments:
            coord -- string representing the coordinates of the cell to be
                     returned

        Raises:
            UnexistingCellException

        Returns:
            Cell: cell in the specified coordinates
        """
        
        if coord in self.cells:
            return self.cells[coord]
        
        raise UnexistingCellException(f"There is no cell with coordinates {coord} in the spreadsheet")
        
    
    def add_content(self, coord:str, content:Content) -> None:
        
        """Set content to a cell of the spreadsheet
        """
        
        cell = self.get_cell(coord)
        cell.set_content(content)

    def get_cell_content(self, coord:str):
        
        """Tries to return the content of a cell. Return None if the cell has
           not been created yet.

        Returns:
            Content: Content at the corresponding cell
        """
        
        if coord in self.cells:
            return self.cells[coord].get_content()
        else:
            return None
    

    def get_all_cell_coordinates(self) -> list:
        return list(self.cells.keys())
    
    
    def cell_exists(self, coord) -> bool:
        
        """Checks whether there is a cell created with an specific coordiantes

        Returns:
           bool: True if a cell with that coordinates exists. Otherwise, return False.
        """
        
        if coord in self.cells:
            return True
        return False
        