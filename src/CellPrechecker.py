import re
from Spreadsheet import Spreadsheet

from UnexistingCellException import UnexistingCellException
from BadCoordinateException import BadCoordinateException

class CellPrechecker:
    
    @staticmethod
    def check_coordinates_validity(coord:str) -> bool:
        
        pattern = re.compile(r'^[A-Z]+[1-9]\d*$')
        
        if not pattern.match(coord):
            raise BadCoordinateException
        
        return True
    
    @staticmethod
    def check_if_cell_exists(spreadsheet:Spreadsheet, coord:str) -> bool:
        
        try:
            cell = spreadsheet.get_cell(coord)
            return True
        except UnexistingCellException:
            return False