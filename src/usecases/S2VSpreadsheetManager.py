import os

from src.usecases.SpreadsheetManager import SpreadsheetManager
from src.entities.Spreadsheet import Spreadsheet
from src.entities.Cell import Cell
from src.entities.Formula import Formula
from src.entities.Numerical import Numerical
from src.entities.Textual import Textual
from src.usecases.FormulaComputer import FormulaComputer
from src.usecases.CellPrechecker import CellPrechecker
from src.usecases.CellFactory import CellFactory

from src.exceptions.ReadingSpreadSheetException import ReadingSpreadsheetException

class S2VSpreadsheetManager(SpreadsheetManager):
    
    
    def __init__(self):
        pass


    def check_content_type(self, str_content:str) -> str:

        """Returns the content type corresponding to a string

        Returns:
            str: "numerical" if correspond to Numerical content. "formula" if
            it correspond to Formula content. "textual" if it corresponds to
            Textual content.
        """
            
        try:
            _ = float(str_content)
            return "numerical"
        except ValueError:
            if str_content.startswith("="):
                return "formula"
            else:
                return "textual"


    def __generate_next_column__(self, col:str):
        
        """Given a column of the spreadsheet, it returns which is the next
        column (e.g. given 'AB', it must return 'AC').
        """
        
        
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
        
        """Returns the index of the last element of a list
        that thas not correspond to an empty string. If none
        correspond to an empty string, return None.
        """
        
        for i in range(len(lst) - 1, -1, -1):
            if lst[i] != '':
                return i
        return None

    
    def save(self, spreadsheet:Spreadsheet, file_path:str) -> None:
        
        """Stores a spreadsheet in the given path
        """
        
        max_row = spreadsheet.get_max_row()
        max_col = spreadsheet.get_max_col()
        coordinates = spreadsheet.get_all_cell_coordinates()
        
        # String that will store the spreadsheet in S2V format
        spreadsheet_str = ''
        
        # Iterate over each row with content
        for current_row in range(1, max_row+1):
            
            # List to store the content at all cells in the row
            row_content = list()
            
            # Iterate over each column of the spreadsheet
            current_col = 'A'
            while True:
                current_coord = current_col + str(current_row)
                
                # If there is no cell in this coordinate, the value is an empty
                # string
                if current_coord not in coordinates:
                    value = ''
                # If there is a get, get its content
                else:
                    content = spreadsheet.get_cell_content(current_coord)
                    
                    if type(content) == Numerical:
                        value = content.get_value()
                        # If the numerical content can be expressed as integer,
                        # remove the decimals
                        if value == int(value):
                            value = str(int(value))
                        # If it has decimals, keep them
                        else:
                            value = str(value) 
                    elif type(content) == Textual:
                        value = content.get_value()
                    # If the content is of type Formula, get the expression and
                    # replace ';' by ','
                    else:
                        value = content.get_content()
                        value = value.replace(';', ',')
                
                row_content.append(value)
                
                # If there are no more columns to iterate over, go to the next
                # row
                if current_col == max_col:
                    break
                # Otherwise, go to the next column
                current_col = self.__generate_next_column__(current_col)
            
            # Get the index of the last column to be stored, i.e. the last
            # column with a value different than an empty string
            last_index = self.find_latest_non_empty_string_index(row_content)
            
            # If there are values to be stored, add them to the S2V string
            if len(row_content) > 0 and last_index is not None:
                row_content = row_content[:last_index+1]
                
                row_str = ';'.join(row_content)
                spreadsheet_str = spreadsheet_str + row_str
            
            spreadsheet_str = spreadsheet_str + '\n'
            
        file = open(file_path, "w")
        file.write(spreadsheet_str)
        file.close()


    def load(self, file_path:str) -> Spreadsheet:
        
        """Tries to load an spreadsheet from a given file

        Raises:
            ReadingSpreadsheetException

        Returns:
            Spreadsheet: The spreadsheet correponding to the file in the given
                         path.
        """
        
        if not os.path.isfile(file_path):
            raise ReadingSpreadsheetException(f"File {file_path} does not exists")
        
        # Create a new spreadsheet
        spreadsheet = Spreadsheet()
        
        # Read the content of the file and split it in lines
        file = open(file_path, 'r')
        lines = file.readlines()
        
        # List to store the coordinates at which there is formula content
        coordinates_formulas = list()
        elements_formulas = list()
        
        # Iterate over eack row (line)
        current_row = 1
        for line in lines:
            
            # Separate the elements of the row
            elements_list = line.split(';')
            
            # Iterate over each column of this row
            current_col = 'A'
            for element in elements_list:
                current_coord = current_col + str(current_row)

                # Remove end of line character (if any)
                element = element.rstrip()
                
                content_type = self.check_content_type(element)
                if content_type == 'formula':
                    element = element.replace(',', ';')
                try: spreadsheet.set_cell_content(current_coord, element, content_type)
                except Exception as ex:
                    coordinates_formulas.append(current_coord)
                    elements_formulas.append(element)
                
                
                # Get the next column to iterate over
                current_col = self.__generate_next_column__(current_col)
            
            current_row = current_row + 1
        
        
        n_formulas = len(coordinates_formulas)
        while n_formulas > 0:
            coord = coordinates_formulas.pop(0)
            element = elements_formulas.pop(0)
            try:
                spreadsheet.set_cell_content(coord, element, "formula")
                n_formulas -= 1
            except Exception as ex:
                coordinates_formulas.append(current_coord)
                elements_formulas.append(element)
        
        return spreadsheet