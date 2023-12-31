class Spreadsheet:
    def __init__(self, data):
        self.data = data

    def get_cell_content(self, coord):
        row, col = coord
        return self.data[row][col]

def print_spreadsheet(spreadsheet):
    max_lengths = [max(len(str(spreadsheet.get_cell_content((row, col))))
                      for row in range(len(spreadsheet.data)))
                   for col in range(len(spreadsheet.data[0]))]

    for row in range(len(spreadsheet.data)):
        for col in range(len(spreadsheet.data[0])):
            cell_content = str(spreadsheet.get_cell_content((row, col)))
            print(f"| {cell_content: <{max_lengths[col]}} ", end="")
        print("\n" + "-" * (sum(max_lengths) + 4 * len(max_lengths)))

# Example usage:
data = [
    ["Name", "Age", "City"],
    ["", '', ''],
    ["Jane Smith", 25, "San Francisco"],
    ["Bob Johnson", 40, "Los Angeles"]
]

spreadsheet = Spreadsheet(data)
print_spreadsheet(spreadsheet)
