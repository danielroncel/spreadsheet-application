from abc import abstractmethod 
from Spreadsheet import Spreadsheet

class SpreadsheetPrinter:
    
    @abstractmethod
    def print(self, spreadsheet:Spreadsheet) -> None:
        pass