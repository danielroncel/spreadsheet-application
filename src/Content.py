from abc import ABC, abstractmethod

class Content(ABC):

    @abstractmethod
    def get_value(self):
        pass