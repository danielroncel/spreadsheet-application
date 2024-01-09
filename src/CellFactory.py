from Cell import Cell

class CellFactory:
    
    @staticmethod
    def create_cell(spreadsheet, coord:str):
        spreadsheet.create_cell(coord)