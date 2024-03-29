from src.usecases.SpreadsheetPrinter import SpreadsheetPrinter
from src.entities.Spreadsheet import Spreadsheet
from src.entities.Numerical import Numerical
from src.entities.Formula import Formula
from src.entities.Textual import Textual

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
        
        """Print a spreadsheet as a grid showing the values of textual and
        numerical content and, additionally, the formula expression for
        formula content.
        
        Arguments:
            spreadsheet {Spreadsheet} -- Spreadsheet to be printed
        """
        
        coords = spreadsheet.get_all_cell_coordinates()
        max_col = spreadsheet.get_max_col()
        max_row = spreadsheet.get_max_row()
        
        if len(coords) == 0:
            return
        
        values = []
        for coord in coords:
            
            if spreadsheet.cell_exists(coord):
                content = spreadsheet.get_cell_content(coord)    

                if type(content) == Numerical:
                    value = content.get_value()
                    
                    if value == int(value):
                        value = str(int(value))
                    else:
                        value = str(value)
                elif type(content) == Textual:
                    value = content.get_value()
                else:
                    expression = content.get_content()
                    value = content.get_value()
                    
                    if value == int(value):
                        value = str(int(value))
                    else:
                        value = str(value)
                            
                    value = expression + '(' + value + ')'
                                
            values.append(value)
            
        max_length = len(max(values, key=len))
        
        print("\n")
        
        for current_row in range(1, max_row+1):
            
            current_col = 'A'
            while True:
                current_coord = current_col + str(current_row)
                
                if spreadsheet.cell_exists(current_coord):
                    content = spreadsheet.get_cell_content(current_coord)    

                    if type(content) == Numerical:
                        value = content.get_value()
                        
                        if value == int(value):
                            value = str(int(value))
                        else:
                            value = str(value)
                    elif type(content) == Textual:
                        value = content.get_value()
                    else:
                        expression = content.get_content()
                        value = content.get_value()
                        
                        if value == int(value):
                            value = str(int(value))
                        else:
                            value = str(value)
                                
                        value = expression + '(' + value + ')'
                else:
                    value = ''
                    
                print(f"| {value.ljust(max_length)[:max_length]}", end='')
                
                if current_col == max_col:
                    break
                
                current_col = BasicSpreadsheetPrinter.__generate_next_column__(current_col)
            
            print()