from Content import Content

class Textual(Content):
    
    def __init__(self, str_content):
        self.value = str_content
        
        
    def get_value(self):
        return self.value