from Content import Content

####### REESCRIBIR. ESTO ES PARA TESTEAR SAVE

class Formula(Content):
    
    def __init__(self, str_content):
        self.value = str_content
        
        
    def get_value(self):
        return self.value