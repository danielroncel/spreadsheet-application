from SpreadsheetManager import SpreadsheetManager
from Spreadsheet import Spreadsheet
from Formula import Formula

class S2VSpreadsheetManager(SpreadsheetManager):
    
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
    
    
    def find_latest_non_empty_string_index(self, lst):
        for i in range(len(lst) - 1, -1, -1):
            if lst[i] != '':
                return i
        return None

    
    def save(self, spreadsheet:Spreadsheet, file_path:str) -> None:
        max_row = spreadsheet.get_max_row()
        max_col = spreadsheet.get_max_col()
        
        spreadsheet_str = ''
        
        for current_row in range(1, max_row+1):
            
            row_content = list()
            
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
                    
                cell_type = spreadsheet.get_cell_type(current_coord)
                if cell_type == Formula:
                    value = value.replace(';', ',')
                    
                row_content.append(value)
                
                if current_col == max_col:
                    break
                
                current_col = S2VSpreadsheetManager.__generate_next_column__(current_col)
                
            last_index = self.find_latest_non_empty_string_index(row_content)
            
            if len(row_content) > 0 and last_index is not None:
                row_content = row_content[:last_index+1]
                
                row_str = ';'.join(row_content)
                spreadsheet_str = spreadsheet_str + row_str
            
            spreadsheet_str = spreadsheet_str + '\n'
            
        file = open(file_path, "w")
        file.write(spreadsheet_str)
        file.close()

    def load(self, file_path:str) -> Spreadsheet:
        pass