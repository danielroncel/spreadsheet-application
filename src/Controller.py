from SpreadsheetMarkerForStudents.usecasesmarker.spreadsheet_controller_for_checker import ISpreadsheetControllerForChecker
from Spreadsheet import Spreadsheet
from CellPrechecker import CellPrechecker
from CellFactory import CellFactory
from Numerical import Numerical
from Textual import Textual
from Formula import Formula

# Leer documentación Juan Carlos para implementar
# BadCoordinateException, NoNumberException, ReadingSpreadSheetException, SavingSpreadSheetException, ContentException, CircularDependencyException

class Controller(ISpreadsheetControllerForChecker):

    def __init__(self):
        self.spreadsheet = Spreadsheet()


    def get_cell_content_as_float(self, coord):
        # Implement the method according to the specification
        pass
        

    def get_cell_content_as_string(self, coord):
        # Implement the method according to the specification
        pass


    def get_cell_formula_expression(self, coord):
        # Implement the method according to the specification
        pass


    def load_spreadsheet_from_file(self, s_name_in_user_dir):
        # Implement the method according to the specification
        pass


    def save_spreadsheet_to_file(self, s_name_in_user_dir):
        # Implement the method according to the specification
        pass


    def set_cell_content(self, coord, str_content):
        
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
    
    
    def check_content_type(str_content:str) -> str:
        
        if str_content.isdigit():
            return "numerical"
        elif str_content.startswith("="):
            return "formula"
        return "textual"