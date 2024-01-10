
class CellComparator:
    
    def __init__(self):
        pass

    def compare_columns(self, col_a:int, col_b:int):
        
        """Returns 1 if col_a goes first than col_b in the spreadsheet.
        Returns -1 if col_b goes first. If both are the same column, return 0.
        
        Examples:
            compare_columns('A', 'B') -> 1
            compare_columns('AA', 'A') -> -1
        """
        
        if len(col_a) < len(col_b):
            return 1
        elif len(col_a) > len(col_b):
            return -1
        else:
            if col_a == col_b:
                return 0
            elif col_a < col_b:
                return 1
            else:
                return -1
            
    def compare_rows(self, row_a:str, row_b:str):
        
        """Returns 1 if row_a goes first than row_b in the spreadsheet.
        Returns -1 if row_b goes first. If both are the same row, return 0.
        
        Examples:
            compare_columns(5, 10) -> 1
            compare_columns(4, 2) -> -1
        """
        
        if row_a == row_b:
            return 0
        elif row_a < row_b:
            return 1
        else:
            return -1