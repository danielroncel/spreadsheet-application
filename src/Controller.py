from SpreadsheetMarkerForStudents.usecasesmarker.spreadsheet_controller_for_checker import ISpreadsheetControllerForChecker
from Spreadsheet import Spreadsheet
from CellPrechecker import CellPrechecker
from CellFactory import CellFactory
from Numerical import Numerical
from Textual import Textual
from Formula import Formula
from BasicSpreadsheetPrinter import BasicSpreadsheetPrinter
from S2VSpreadsheetManager import S2VSpreadsheetManager

from SpreadsheetMarkerForStudents.entities.bad_coordinate_exception import BadCoordinateException
from SpreadsheetMarkerForStudents.entities.no_number_exception import NoNumberException


class Controller(ISpreadsheetControllerForChecker):

    def __init__(self):
        self.spreadsheet = Spreadsheet()
        self.spreadsheet_printer = BasicSpreadsheetPrinter()
        self.spreadsheet_manager = S2VSpreadsheetManager()


    def create_new_spreadsheet(self):
        
        """Set to the controller a new and empty spreadsheet
        """
        
        self.spreadsheet = Spreadsheet()


    def get_cell_content_as_float(self, coord):
        
        """Returns the value of the content of a cell as a float

        Arguments:
            coord -- a string representing a coordinate in spreadsheet

        Raises:
            NoNumberException

        Returns:
            float: the value of the content of a cell. If the cell contains a
                   textual content whose value is the textual representation of
                   a number, it shall return this number. If the cell contains
                   a numerical content, it just returns its value. If the cell
                   contentis a formula, it returns the number resulting of
                   evaluating such formula.
        """
        
        CellPrechecker.check_coordinates_validity(coord)
        
        if self.spreadsheet.cell_exists(coord):
            content = self.spreadsheet.get_cell_content(coord)
            
            if type(content) == Textual:
                raise NoNumberException
            
            return content.get_value()
                

    def get_cell_content_as_string(self, coord):
        
        """Returns a string version of the content of a cell
        
        Arguments:
            coord -- a string representing a coordinate in spreadsheet

        Returns:
            str: string version of the content of a cell. If the cell contains
                 a textual content it directly shall return its string value.
                 If the cell contains a numerical content, it returns the
                 textual representation of the number . If the cell content is
                 a formula, it returns the string representing the number
                 resulting of evaluating such formula.
        """
        
        CellPrechecker.check_coordinates_validity(coord)
        
        
        if self.spreadsheet.cell_exists(coord):
            content = self.spreadsheet.get_cell_content(coord)
            
            
            if type(content) == Numerical:
                value = content.get_value()
                
                if value == int(value):
                    return str(int(value))
                return str(value)
                                
            elif type(content) == Textual:
                return content.get_value()
            else:
                return content.get_expression()
        
        return ''
            

    def get_cell_formula_expression(self, coord):
        
        """Returns the textual representation of the formula present in the
           cell whose coordiantes are represented by argument coord

        Arguments:
            coord -- a string representing a coordinate in spreadsheet

        Raises:
            BadCoordinateException: _description_
            BadCoordinateException: _description_

        Returns:
            str: textual representation of a formula
        """
        
        CellPrechecker.check_coordinates_validity(coord)

        if self.spreadsheet.cell_exists(coord):
            content = self.spreadsheet.get_cell_content(coord)
            
            if type(content) == Formula:
                expression = content.get_expression()

                return expression
                
            else:
                raise BadCoordinateException
        else:
            raise BadCoordinateException
        

    def load_spreadsheet_from_file(self, s_name_in_user_dir):
        
        """Tries to load the spreadsheet from a file.

        Arguments:
            s_name_in_user_dir -- path of the file to be loaded as a
                                  spreadsheet
        """
        
        # Implement the method according to the specification
        self.spreadsheet = self.spreadsheet_manager.load(s_name_in_user_dir)


    def save_spreadsheet_to_file(self, s_name_in_user_dir):

        """Tries to save the spreadsheet into a file.

        Arguments:
            s_name_in_user_dir -- path in which to save the spreadsheet
        """

        self.spreadsheet_manager.save(self.spreadsheet, s_name_in_user_dir)


    def set_cell_content(self, coord, str_content):
        
        """Tries to set the content of a cell of the spreadsheet in a certain
        coordinate.

        Arguments:
            coord -- a string representing a coordinate in spreadsheet
            str_content -- string that represents the content to be stored in
                           the cell
        """
        
        """
        Dudas:
        1. Si en add_content se lanza un error...
                ...¿cómo deshacemos la celda creada?
                ...¿cómo modificamos las celdas que fueron modificadas por tener dependencias?
        """
        
        CellPrechecker.check_coordinates_validity(coord)
                
        if not CellPrechecker.check_if_cell_exists(self.spreadsheet, coord):
            CellFactory.create_cell(self.spreadsheet, coord)
            
        content_type = self.check_content_type(str_content)

        if content_type == "numerical":
            content = Numerical(str_content)
        elif content_type == "formula":
            content = Formula(str_content)
        else:
            content = Textual(str_content)

        self.spreadsheet.add_content(coord, content)
    
    
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
    
    
    def print_spreadsheet(self) -> None:
        
        """Print the current spreadsheet
        """
        
        self.spreadsheet_printer.print(self.spreadsheet)