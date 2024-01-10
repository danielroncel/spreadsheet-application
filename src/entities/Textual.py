from src.entities.Content import Content

class Textual(Content):
    
    def __init__(self, str_content):
        self.content = str_content
        self.value = str_content
        
        
    def get_content(self):
        return self.content
    
    def get_value(self):
        return self.value
    
    def set_value(self, value) -> None:
        self.value = value
    
    def set_content(self, content) -> None:
        self.content = content