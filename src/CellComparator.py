import re

from Cell import Cell

class CellComparator:
    
    def compare_rows(row_a:str, row_b:str):
        
        if len(row_a) < len(row_b):
            return 1
        elif len(row_a) > len(row_b):
            return -1
        else:
            if row_a == row_b:
                return 0
            elif row_a < row_b:
                return 1
            else:
                return -1
            
    def compare_columns(col_a:int, col_b:int):
        
        if col_a == col_b:
            return 0
        elif col_a < col_b:
            return 1
        else:
            return -1
       
       
    def compare_cells(coords_a:str, coords_b:str):
        
        match = re.match(r'([A-Z]+)(\d+)', coords_a)
        row_a, col_a = match.groups()
        
        match = re.match(r'([A-Z]+)(\d+)', coords_b)
        row_b, col_b = match.groups()
        
        if row_a == row_b and col_a == col_b:
            return 0
        
        row_comparison = CellComparator.compare_rows(row_a, row_b)
        if row_comparison != 0:
            return row_comparison
        else:
            return CellComparator.compare_columns(col_a, col_b)
            
if __name__ == '__main__':
    
    print(CellComparator.compare_rows('A', 'B'))
    print(CellComparator.compare_rows('AA', 'B'))
    print(CellComparator.compare_rows('AB', 'BA'))
    print(CellComparator.compare_rows('BBA', 'BAB'))
    
    print(CellComparator.compare_columns(1, 2))
    print(CellComparator.compare_columns(12, 20))
    print(CellComparator.compare_columns(122, 2))
    print(CellComparator.compare_columns(8, 12))
    
    print(CellComparator.compare_cells('A1', 'A1'))
    print(CellComparator.compare_cells('A1', 'B1'))
    print(CellComparator.compare_cells('B1', 'A1'))
    print(CellComparator.compare_cells('AA1', 'A1'))