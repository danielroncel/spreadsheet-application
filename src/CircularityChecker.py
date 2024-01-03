from Spreadsheet import Spreadsheet

class CircularityChecker:
    def __init__(self, cellId, spreadsheet, tokens):
        self.cellId = cellId
        self.spreadsheet = spreadsheet
        self.tokens = tokens


    def check_circularities(self):
        visited = [self.cellId]
        for el in self.tokens(self.spreadsheet.is_valid_cell_id(self.tokens)):
            self.dfs(el, visited)
        

    def dfs(self, el, visited):
        for cell in self.spreadsheet.get_el(el).get_depend_on():
                if el == self.cellId:
                    raise Exception("Circularity detected")
                if el not in visited:
                    visited.add(el)
                    self.dfs(el, visited)

