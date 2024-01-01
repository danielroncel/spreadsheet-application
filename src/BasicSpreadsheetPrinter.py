from SpreadsheetPrinter import SpreadsheetPrinter
from Spreadsheet import Spreadsheet

from itertools import permutations

class BasicSpreadsheetPrinter(SpreadsheetPrinter):
    
    def __init__(self):
        pass
    
    def __generate_next_column__(col:str):
        
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


    def print(self, spreadsheet:Spreadsheet) -> None:
        
        coords = spreadsheet.get_all_cell_coordinates()
        max_col = spreadsheet.get_max_col()
        max_row = spreadsheet.get_max_row()
        
        if len(coords) == 0:
            return
        
        values = []
        for coord in coords:
            value = spreadsheet.get_cell_content(coord)
            if type(value) == float:
                if value == int(value):
                    value = str(int(value))
                else:
                    value = str(value)
            values.append(value)
        
        max_length = len(max(values, key=len))
        
        print("\n")
        
        for current_row in range(1, max_row+1):
            
            current_col = 'A'
            while True:
                current_coord = current_col + str(current_row)
                
                value = spreadsheet.get_cell_content(current_coord)
                if value is None:
                    value = ''
                elif type(value) == float:
                    if value == int(value):
                        value = str(int(value))
                    else:
                        value = str(value)
                else:
                    value = str(value)
                    
                print(f"| {value.ljust(max_length)[:max_length]}", end='')
                
                if current_col == max_col:
                    break
                
                current_col = BasicSpreadsheetPrinter.__generate_next_column__(current_col)
            
            print()