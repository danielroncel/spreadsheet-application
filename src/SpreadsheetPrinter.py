from abc import ABC, abstractmethod 
from Spreadsheet import Spreadsheet

class SpreadsheetPrinter(ABC):
    
    @abstractmethod
    def print(self, spreadsheet:Spreadsheet) -> None:
        pass