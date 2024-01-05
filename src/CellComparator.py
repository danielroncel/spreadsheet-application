import re

from Cell import Cell

class CellComparator:
    
    def compare_columns(col_a:int, col_b:int):
        
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
            
    def compare_rows(row_a:str, row_b:str):
        
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
            
if __name__ == '__main__':
    
    print(CellComparator.compare_rows('A', 'B'))
    print(CellComparator.compare_rows('AA', 'B'))
    print(CellComparator.compare_rows('AB', 'BA'))
    print(CellComparator.compare_rows('BBA', 'BAB'))
    
    print(CellComparator.compare_columns(1, 2))
    print(CellComparator.compare_columns(12, 20))
    print(CellComparator.compare_columns(122, 2))
    print(CellComparator.compare_columns(8, 12))