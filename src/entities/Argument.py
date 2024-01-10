from abc import ABC, abstractmethod

class Argument(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def get_value(self):
        pass
    
    @abstractmethod
    def accept_visitor(visitor):
        pass