from Content import Content

class Formula(Content):
    
    def __init__(self, str_content):
        self.expression = str_content
        self.value = None
        
    def get_value(self):
        return self.value
    
    def set_value(self, value):
        self.value = value
        
    def get_expression(self):
        return self.expression
    
    def set_content(self):
        return self.content