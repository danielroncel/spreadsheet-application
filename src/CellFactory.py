from Cell import Cell
from Spreadsheet import Spreadsheet

class CellFactory:
    
    @staticmethod
    def create_cell(spreadsheet:Spreadsheet, coord:str):
        spreadsheet.create_cell(coord)