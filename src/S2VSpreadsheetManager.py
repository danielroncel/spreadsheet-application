import os

from SpreadsheetManager import SpreadsheetManager
from Spreadsheet import Spreadsheet
from Formula import Formula
from Numerical import Numerical
from Textual import Textual
from FormulaComputer import FormulaComputer
from CellPrechecker import CellPrechecker
from CellFactory import CellFactory

from ReadingSpreadSheetException import ReadingSpreadsheetException

class S2VSpreadsheetManager(SpreadsheetManager):
    
    def __init__(self):
        pass

    def __check_content_type__(self, str_content:str) -> str:
            
            try:
                _ = float(str_content)
                return "numerical"
            except ValueError:
                if str_content.startswith("="):
                    return "formula"
                else:
                    return "textual"


    def __generate_next_column__(self, col:str):
        
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
        coordinates = spreadsheet.get_all_cell_coordinates()
        
        spreadsheet_str = ''
        
        for current_row in range(1, max_row+1):
            
            row_content = list()
            
            current_col = 'A'
            while True:
                current_coord = current_col + str(current_row)
                
                if current_coord not in coordinates:
                    value = ''
                else:
                    content = spreadsheet.get_cell_content(current_coord)
                    
                    if type(content) == Numerical:
                        value = content.get_value()
                        # if can be expressed as integer, remove the decimals
                        if value == int(value):
                            value = str(int(value))
                        # if it has decimals, keep them
                        else:
                            value = str(value)
                            
                    elif type(content) == Textual:
                        value = content.get_value()
                        
                    # if the content is of type Formula
                    else:
                        value = content.get_expression()
                        value = value.replace(';', ',')
                        
                row_content.append(value)
                
                if current_col == max_col:
                    break
                
                current_col = self.__generate_next_column__(current_col)
                
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
        
        if not os.path.isfile(file_path):
            raise ReadingSpreadsheetException(f"File {file_path} does not exists")
        
        spreadsheet = Spreadsheet()
        
        file = open(file_path, 'r')
        lines = file.readlines()
        
        current_row = 1
        for line in lines:
            
            elements_list = line.split(';')
            
            current_col = 'A'
            for element in elements_list:
                current_coord = current_col + str(current_row)
                
                if element != '':
                    t = self.__check_content_type__(element)
                    
                    if t == "numerical":
                        content = Numerical(element)
                    elif t == "textual":
                        content = Textual(element)
                    else:
                        content = Formula(element)
                    
                    if not CellPrechecker.check_if_cell_exists(spreadsheet, current_coord):
                        CellFactory.create_cell(spreadsheet, current_coord)
                            
                    spreadsheet.add_content(current_coord, content)
                    
                    #formula_computer = FormulaComputer(spreadsheet, element, )
                
                current_col = self.__generate_next_column__(current_col)
            
            current_row = current_row + 1
            
        return spreadsheet