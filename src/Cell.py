from Content import Content
from Textual import Textual

class Cell:

    def __init__(self, coord:str, content = Textual('')):
        self.coordinate = coord
        self.content = content
        self.I_depend_on = set()
        self.depend_on_me = set()

    def get_content(self):
        return self.content

    def set_content(self, content:Content):
        self.content = content
        
    def get_coordinates(self):
        return self.coordinate
    
    def get_I_depend_on(self):
        return self.I_depend_on
    
    def get_depend_on_me(self):
        return self.depend_on_me
    
    def set_I_depend_on(self,depend: []):
        self.I_depend_on = depend

    def set_depend_on_me(self,depend: []):
        self.depend_on_me = depend
    