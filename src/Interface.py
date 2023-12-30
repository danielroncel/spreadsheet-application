def run_spreadsheet_application():
    current_spreadsheet = None

    while True:
        print("Options:")
        print("1. Edit Cell")
        print("2. Create New Spreadsheet")
        print("3. Load Spreadsheet")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            coordinate = input("Enter cell coordinate: ")
            content = input("Enter new content: ")
            current_spreadsheet.editCell(coordinate, content)
        elif choice == '2':
            current_spreadsheet = createNewSpreadsheet()
        elif choice == '3':
            path = input("Enter path to load spreadsheet: ")
            if not path:
                print("Invalid argument. Please provide a valid path.")
            else:
                loaded_spreadsheet = loadSpreadsheet(path)
                if loaded_spreadsheet:
                    current_spreadsheet = loaded_spreadsheet
        elif choice == '4':
            print("Exiting the spreadsheet application.")
            break
        else:
            print("Invalid choice. Please choose a valid option.")
            
if __name__ == '__main__':
    run_spreadsheet_application()