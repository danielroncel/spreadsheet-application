from abc import abstractmethod 
from Spreadsheet import Spreadsheet

class SpreadsheetManager:
    
    @abstractmethod
    def save(spreadsheet:Spreadsheet, file_path:str) -> None:
        pass
    
    @abstractmethod
    def load(file_path:str) -> Spreadsheet:
        pass