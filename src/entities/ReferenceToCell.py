from src.entities.Operand import Operand
from src.entities.Argument import Argument
from src.usecases.FormulaComputerVisitor import FormulaComputerVisitor

class ReferenceToCell(Operand, Argument):

    def __init__(self,cell_id) -> None:
        self.value = cell_id

    def get_value(self):
        return self.value
    
    def set_value(self,content):
        self.value = content

    def accept_visitor(self,visitor:FormulaComputerVisitor):
        visitor.visit_cell_reference(self)


class RangeOfCells(Argument):
    def __init__(self, ini_cell: str, end_cell: str) -> None:
        self.ini_cell = ini_cell
        self.end_cell = end_cell
        self.value = self.expand_cells()

    def get_value(self) -> []:
        return self.value
    
    def find_first_numerical_index(self,s):
        for i, char in enumerate(s):
            if char.isdigit():
                return i
        
    def expand_cells(self) -> []:    
        first_num_ini = self.find_first_numerical_index(self.ini_cell)
        first_num_end = self.find_first_numerical_index(self.end_cell)
        cells = []
        col = self.ini_cell[:first_num_ini]
        min_row = int(self.ini_cell[first_num_ini:])
        max_col = self.end_cell[:first_num_end]
        max_row = int(self.end_cell[first_num_end:])

        while col <= max_col :
            for row in range(min_row, max_row+1):
                cell = col+str(row)
                cells.append(cell)
            col = self.get_next_column(col)
            
        return cells

    def get_next_column(self, col:str) -> str:
        
        # Convert the coordinate to a numeric value
        numeric_value = 0
        for char in col:
            numeric_value = numeric_value * 26 + (ord(char) - ord('A') + 1)

        # Increment the numeric value
        numeric_value += 1

        # Convert the numeric value back to alphabetical representation
        result_coordinate = ''
        while numeric_value > 0:
            numeric_value, remainder = divmod(numeric_value - 1, 26)
            result_coordinate = chr(remainder + ord('A')) + result_coordinate

        return result_coordinate
    
    def accept_visitor(self,visitor:FormulaComputerVisitor):
        visitor.visit_range_of_cells(self)
    
