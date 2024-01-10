import os

from src.usecases.Controller import Controller
from src.entities.Spreadsheet import Spreadsheet

from src.exceptions.NoSpreadsheetException import NoSpreadsheetException
from src.exceptions.InvalidCommandException import InvalidCommandException

class Interface:

    """Class to create a textual user interface for creating, editing, loading
    and saving spreadsheets.
    """
    
    def __init__(self):
        self.controller = Controller()


    def edit_cell_option(self, command:str) -> None:
        
        """Execute a command that corresponds to editing the content of a cell
        of the current spreadsheet

        Arguments:
            command {str} -- editing cell command
            
        Raises:
            NoSpreadsheetException
            InvalidCommandException
        """
        
        if self.controller.spreadsheet is None:
            raise NoSpreadsheetException("There is no spreadsheet to be edited")

        command_tokens = command.split()
        if len(command_tokens) < 3:
            raise InvalidCommandException("Invalid arguments for E command")
        
        coord = command_tokens[1]
        str_content = ' '.join(command_tokens[2:])
    
        self.controller.set_cell_content(coord, str_content)

    def read_commands_option(self, command:str) -> None:
        
        """Execute a command that corresponds to loading a text file with
        commands and executing them.

        Arguments:
            command {str} -- read commands command

        Raises:
            InvalidCommandException
            FileNotFoundError
        """
        
        if len(command.split()) != 2:
            raise InvalidCommandException("Invalid arguments for RF command")
        
        file_path = command.split()[1]
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist")
        
        file = open(file_path, 'r')
        commands_list = file.readlines()
        
        for command in commands_list:
            self.execute_command(command)
        

    def load_spreadsheet_option(self, command:str) -> None:

        """Execute a command that corresponds to loading and spreadsheet
        from disk
        
        Arguments:
            command {str} -- Loading command

        Raises:
            InvalidCommandException: _description_
        """
        
        if len(command.split()) != 2:
            raise InvalidCommandException("Invalid arguments for L command")
        
        file_path = command.split()[1]
        
        self.controller.load_spreadsheet_from_file(file_path)


    def save_spreadsheet_option(self, command:str) -> None:
        
        """Execute a command that corresponds to saving the current spreadsheet
        to disk
        
        Arguments:
            command {str} -- Saving command

        Raises:
            InvalidCommandException
        """
        
        if len(command.split()) != 2:
            raise InvalidCommandException("Invalid arguments for S command")
        
        file_path = command.split()[1]
        
        self.controller.save_spreadsheet_to_file(file_path)
        
        
    def execute_command(self, command:str) -> None:
        
        """Execute a command
        
        Arguments:
            command {str} -- String representing the command

        Raises:
            InvalidCommandException
        """
        
        # Parse input intems
        option = command.split()[0]
        
        if option == 'C':
            self.controller.spreadsheet = Spreadsheet()
        elif option == 'L':
            self.load_spreadsheet_option(command)
        elif option == 'S':
            self.save_spreadsheet_option(command)
        elif option == 'E':
            self.edit_cell_option(command)
        elif option == 'RF':
            self.read_commands_option(command)
        elif option == 'Q':
            print("Closing the application...")
            exit()
        else:
            raise InvalidCommandException("The command introduced is not valid")
    
    
    def run_spreadsheet_application(self):
        
        """Method to start running the UI
        """
        
        while True:
            
            print("\nOptions:")
            print("Read commands from file (RF <text file pathname>)")
            print("Create a new spreadsheet (C)")
            print("Edit a cell (E <cell coordinate> <new cell content>)")
            print("Load a spreadsheet from a file (L <SV2 file pathname>)")
            print("Save the spreadsheet to a file (S <SV2 file pathname>)")
            print("Close application (Q)")
            
            user_input = input(": ")
            
            try: 
                self.execute_command(user_input)
            except Exception as ex:
                print(ex)
                
            self.controller.print_spreadsheet()
        
            
if __name__ == '__main__':
    interface = Interface()
    interface.run_spreadsheet_application()