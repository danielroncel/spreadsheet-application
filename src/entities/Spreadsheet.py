import re

from src.entities.Cell import Cell
from src.entities.Content import Content
from src.usecases.CellComparator import CellComparator
from src.usecases.FormulaComputer import FormulaComputer, FormulaRecomputer
from src.exceptions.UnexistingCellException import UnexistingCellException
from src.usecases.CellPrechecker import CellPrechecker
from src.usecases.CellFactory import CellFactory
from src.entities.FormulaContent import FormulaContent
from src.usecases.CircularityChecker import CircularityChecker
from src.entities.Numerical import Numerical
from src.entities.Textual import Textual
from src.entities.Formula import Formula

class Spreadsheet:
    
    def __init__(self):
        self.cells = dict()
        self.max_col = 'A'
        self.max_row = 1
        self.formula_computer = FormulaComputer(self)
        self.formula_recomputer = FormulaRecomputer(self)
        self.cell_comparator = CellComparator()
        self.cell_prechecker = CellPrechecker()
        self.cell_factory = CellFactory()
        self.circularity_checker = CircularityChecker(self)
    
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
            if self.cell_comparator.compare_columns(self.max_col, col) == 1:
                self.max_col = col
            # Update which is the row more distance of 'A' column with
            # a created cell
            if self.cell_comparator.compare_rows(self.max_row, int(row)) == 1:
                self.max_row = int(row)
        
            
    def get_max_row(self) -> int:
        return self.max_row
    
    
    def get_max_col(self) -> str:
        return self.max_col
    
    
    def get_cell_content(self, coord:str):
        
        if coord in self.cells:
            return self.cells[coord].get_content()
        else:
            return None
    
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
        if coord not in self.cells:
            self.cell_factory.create_cell(self,coord)
        
        return self.cells[coord]
        
    
    def add_content(self, coord:str, content:Content) -> None:
        
        """Set content to a cell of the spreadsheet
        """
        
        cell = self.get_cell(coord)
        cell.set_content(content)
    
    def get_cell_type(self, coord:str):
        
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
    
    def check_for_circularities(self, expr: FormulaContent, cell_id):
        dependent_cells = self.circularity_checker.get_referenced_cells(expr)   
        self.circularity_checker.check_circularities(cell_id, dependent_cells)

    def update_dependencies(self, dependent,cell_id):
        prev_dependencies = self.get_cell(cell_id).get_I_depend_on()
        
        self.get_cell(cell_id).set_I_depend_on(dependent)
        for el in prev_dependencies:
            if el not in dependent:
                arr = self.get_cell(el).get_depend_on_me()
                arr.remove(cell_id)
                self.get_cell(el).set_depend_on_me(arr)
        
        for s in  dependent:
            if s not in prev_dependencies:
                arr = self.get_cell(s).get_depend_on_me()
                arr.add(cell_id)
                self.get_cell(s).set_depend_on_me(arr)
    

    def recompute_dependent_cells(self,cell_id):
        self.formula_recomputer.recompute_dependent_cell(cell_id)

    def cell_exists(self, coord) -> bool:
        
        """Checks whether there is a cell created with an specific coordiantes

        Returns:
           bool: True if a cell with that coordinates exists. Otherwise, return False.
        """
        
        if coord in self.cells:
            return True
        return False
    
    def set_cell_content(self, coord, str_content, content_type):
        
        """Tries to set the content of a cell of the spreadsheet in a certain
        coordinate.

        Arguments:
            coord -- a string representing a coordinate in spreadsheet
            str_content -- string that represents the content to be stored in
                           the cell
        """
        
        try: self.cell_prechecker.check_coordinates_validity(coord)
        except Exception as ex: raise ex

        if content_type == "numerical":
            content = Numerical(str_content)
            value = float(str_content)
            dependent_cells = set()
        elif content_type == "formula":
            try:
                value,formula_content, dependent_cells = self.formula_computer.compute_formula_value(str_content,coord)
                content = Formula(str_content, value, formula_content)
            except Exception as e:
                raise e
        else:
            content = Textual(str_content)
            value = str_content
            dependent_cells = set()
    
        if not self.cell_prechecker.check_if_cell_exists(self, coord):
            self.cell_factory.create_cell(self, coord)
        
        self.add_content(coord, content)
        
        self.update_dependencies(dependent_cells, coord)
        
        if self.get_cell(coord).get_depend_on_me():
            self.recompute_dependent_cells(coord)
