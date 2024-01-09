import re

from UnexistingCellException import UnexistingCellException
from SpreadsheetMarkerForStudents.entities.bad_coordinate_exception import BadCoordinateException

class CellPrechecker:
    def __init(self):
        pass
    
    def check_coordinates_validity(self, coord:str) -> bool:
        
        pattern = re.compile(r'^[A-Z]+[1-9]\d*$')
        
        if not pattern.match(coord):
            raise BadCoordinateException(f"Coordinates {coord} are unvalid")
        
        return True
    
    
    def check_if_cell_exists(self, spreadsheet, coord:str) -> bool:
        
        try:
            cell = spreadsheet.get_cell(coord)
            return True
        except UnexistingCellException:
            return False