from Content import Content

class Numerical(Content):
    
    def __init__(self, str_content):
        self.value = float(str_content)
                
    def get_value(self):
        return self.value