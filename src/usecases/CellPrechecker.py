import re

from src.SpreadsheetMarkerForStudents.entities.bad_coordinate_exception import BadCoordinateException

class CellPrechecker:
    
    def __init(self):
        pass
    
    def check_coordinates_validity(self, coord:str) -> bool:
        
        """Check whether the coordinate is valid. To be valid, it
        must correspond to a sequence of letters (to indicate the column)
        followed by a sequence of digits (to indicate the row).

        Raises:
            BadCoordinateException

        Returns:
            bool: True if the coordinate is valid. Otherwise, it raises
                  a BadCoordinateException.
        """
        
        pattern = re.compile(r'^[A-Z]+[1-9]\d*$')
        
        if not pattern.match(coord):
            raise BadCoordinateException(f"Coordinates {coord} are unvalid")
        
        return True
    
    
    def check_if_cell_exists(self, spreadsheet, coord:str) -> bool:
        
        """Return True if there is a cell created in the spreadsheet with the
        specified coordinates. Otherwise, return False.

        Returns:
            _type_: _description_
        """
        
        try:
            cell = spreadsheet.get_cell(coord)
            return True
        except:
            return False