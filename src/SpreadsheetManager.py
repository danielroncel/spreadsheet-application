from abc import ABC, abstractmethod 
from Spreadsheet import Spreadsheet

class SpreadsheetManager(ABC):
    
    @abstractmethod
    def save(spreadsheet:Spreadsheet, file_path:str) -> None:
        pass
    
    @abstractmethod
    def load(file_path:str) -> Spreadsheet:
        pass