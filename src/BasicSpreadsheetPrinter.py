from SpreadsheetPrinter import SpreadsheetPrinter
from Spreadsheet import Spreadsheet

class BasicSpreadsheetPrinter(SpreadsheetPrinter):
    
    def __init__(self):
        pass
    
    def print(self, spreadsheet:Spreadsheet) -> None:
        
        coords = spreadsheet.get_all_cell_coordinates()
        
        if len(coords) == 0:
            print()
            
        for coord in coords:
            content_value = spreadsheet.get_cell_content(coord)
            
            if content_value is None:
                content_str  = ''
            elif type(content_value) == float:
                content_str = str(content_value)
            else:
                content_str = content_value
                
            print(f"{coord}: {content_str}")