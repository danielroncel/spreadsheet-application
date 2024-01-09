from abc import ABC, abstractmethod

class Content(ABC):

    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def get_content(self):
        pass