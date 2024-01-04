from Controller import Controller

if __name__ == '__main__':
    
    controller = Controller()
    
    controller.set_cell_content("A3", "=10*2")
    
    formula = controller.get_cell_formula_expression("A3")
    
    print(formula)