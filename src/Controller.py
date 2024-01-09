from SpreadsheetMarkerForStudents.usecasesmarker.spreadsheet_controller_for_checker import ISpreadsheetControllerForChecker
from Spreadsheet import Spreadsheet
from CellPrechecker import CellPrechecker
from CellFactory import CellFactory
from Numerical import Numerical
from Textual import Textual
from Formula import Formula
from BasicSpreadsheetPrinter import BasicSpreadsheetPrinter
from S2VSpreadsheetManager import S2VSpreadsheetManager
from FormulaComputer import FormulaComputer

from SpreadsheetMarkerForStudents.entities.bad_coordinate_exception import BadCoordinateException
from SpreadsheetMarkerForStudents.entities.no_number_exception import NoNumberException

# Leer documentación Juan Carlos para implementar
# BadCoordinateException, NoNumberException, ReadingSpreadSheetException, SavingSpreadSheetException, ContentException, CircularDependencyException

class Controller(ISpreadsheetControllerForChecker):

    def __init__(self):
        self.spreadsheet = Spreadsheet()
        self.spreadsheet_printer = BasicSpreadsheetPrinter()
        self.spreadsheet_manager = S2VSpreadsheetManager()


    def create_new_spreadsheet(self):
        self.spreadsheet = Spreadsheet()


    def get_cell_content_as_float(self, coord):
        # Implement the method according to the specification
        self.spreadsheet.cell_prechecker.check_coordinates_validity(coord)
        
        content_value = self.spreadsheet.get_cell_content(coord)
        if content_value is None or type(content_value) == str:
            raise NoNumberException("Not a number")
        else:
            return content_value


    def get_cell_content_as_string(self, coord):
        # Implement the method according to the specification
        self.spreadsheet.cell_prechecker.check_coordinates_validity(coord)
        
        content_value = self.spreadsheet.get_cell_content(coord)
        
        if content_value is None:
            return ''
        elif type(content_value) == float:
            return str(content_value)
        else:
            return content_value
            

    def get_cell_formula_expression(self, coord):
        # Implement the method according to the specification
        pass


    def load_spreadsheet_from_file(self, s_name_in_user_dir):
        # Implement the method according to the specification
        self.spreadsheet = self.spreadsheet_manager.load(s_name_in_user_dir)


    def save_spreadsheet_to_file(self, s_name_in_user_dir):
        # Implement the method according to the specification
        self.spreadsheet_manager.save(self.spreadsheet, s_name_in_user_dir)


    def set_cell_content(self, coord, str_content):
        
        """
        Dudas:
        1. Si en add_content se lanza un error...
                ...¿cómo deshacemos la celda creada?
                ...¿cómo modificamos las celdas que fueron modificadas por tener dependencias?
        """
        self.spreadsheet.cell_prechecker.check_coordinates_validity(coord)
            
            
        content_type = self.check_content_type(str_content)

        if content_type == "numerical":
            content = Numerical(str_content)
            value = float(str_content)
        elif content_type == "formula":
            #TODO. Compute formula value and store it appart
            try:
                value,formula_content, dependent_cells = self.spreadsheet.compute_formula_value(str_content, coord)
                content = Formula(str_content, formula_content)
            except Exception as e: 
                print(f"An error occurred: {e}")
                return
            
        else:
            content = Textual(str_content)
            value = str_content
    
        if not self.spreadsheet.cell_prechecker.check_if_cell_exists(self.spreadsheet, coord):
            self.spreadsheet.cell_factory.create_cell(self.spreadsheet, coord)
        
        self.spreadsheet.add_content(coord, content)
        self.spreadsheet.add_value(coord, value)
        
        if content_type == 'formula':
            self.spreadsheet.get_cell(coord).set_I_depend_on(dependent_cells)
            self.spreadsheet.update_dependencies(dependent_cells,coord)
        self.spreadsheet.recompute_dependent_cells(coord)

    def check_content_type(self, str_content:str) -> str:
        
        try:
            _ = float(str_content)
            return "numerical"
        except ValueError:
            if str_content.startswith("="):
                return "formula"
            else:
                return "textual"
    
    
    def print_spreadsheet(self) -> None:
        self.spreadsheet_printer.print(self.spreadsheet)

controller = Controller()
controller.set_cell_content("A1","1")
controller.set_cell_content("A1","1")
controller.set_cell_content("A2","2")
controller.set_cell_content("A3","3")
controller.set_cell_content("A4","4")
controller.set_cell_content("A5","5")
controller.set_cell_content("A6","6")
controller.set_cell_content("A7","7")
controller.set_cell_content("A8","8")
controller.set_cell_content("A9","9")
controller.set_cell_content("A10","10")
controller.set_cell_content("A11","11")
controller.set_cell_content("A12","12")
controller.set_cell_content("A13","13")
controller.set_cell_content("A14","14")
controller.set_cell_content("A15","15")
controller.set_cell_content("A16","16")
controller.set_cell_content("A17","17")
controller.set_cell_content("A18","18")
controller.set_cell_content("A19","19")
controller.set_cell_content("A20","20")
controller.set_cell_content("A21","21")
controller.set_cell_content("A22","22")
controller.set_cell_content("A23","23")
controller.set_cell_content("A24","24")
controller.set_cell_content("A25","This is a string")
controller.set_cell_content("J1", "=(A5*4)/(A2+A2)+SUMA(A1;A2;3;4;5;A6:A12;MIN(A13:A20))")
controller.set_cell_content('B1','=A1+2-A2')
controller.set_cell_content('A1','2')
val = controller.get_cell_content_as_float('B1')
print(val)
"""set_cell_content("I1", "=(A5*4)/(A2+A2)+SUMA(A1;A2;3;4;5;A6:A12)")
set_cell_content("J1", "=(A5*4)/(A2+A2)+SUMA(A1;A2;3;4;5;A6:A12;MIN(A13:A20))")
set_cell_content("C1", "=2+SUMA(A6:A10)")"""


