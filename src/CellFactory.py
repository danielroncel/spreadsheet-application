from Cell import Cell

class CellFactory:
    
    def create_cell(self, spreadsheet, coord:str):
        spreadsheet.create_cell(coord)