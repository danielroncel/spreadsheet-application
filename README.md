To use the spreadheet application:
    - Open the python project on this folder, i.e. the root folder of the repository. Othewise, there might be error when importing the files.
    - Run src/Interface.py.
    - The interface satisfies the requirements specified by the teacher for a text-based user interface. Thus, the commands to interact with it are the following:
        - Create a new spreadsheet: C
        - Editing one cell: E <cell_coordinate>, <new_cell_content> (e.g. E D3 4)
        - Loading a spreadsheet: L <S2V_file_path>
        - Saving a spreadsheet: S <S2V_file_path>
        - Executing commands from a file: RF <text_file_path>
    - The path from which the files are read are taking as root the root of this repository.
    - To test command RF, we have created ejemplo_comando_rf.txt

To execute the automtic marker:
    - Open the python project on this folder, i.e. the root folder of the repository. Othewise, there might be error when importing the files.
    - Run src/SpreadsheetMarkerForStudents/markerrun/TestRunner.py

Important notes:
    - It might be possible the need to install git library. To do so, execute the following command:
        pip install GitPython