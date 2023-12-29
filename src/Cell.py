from Content import Content

class Cell:
    
    def __init__(self, coord:str):
        self.coordinate = coord
        
        self.content = None
        self.I_depend_on = []
        self.depend_on_me = []


    def __init__(self, coord:str, content:Content):
        self.coordinate = coord
        self.content = content

        self.I_depend_on = []
        self.depend_on_me = []


    def getContent(self):
        return self.content


    def set_content(self, content:Content):
        self.content = content