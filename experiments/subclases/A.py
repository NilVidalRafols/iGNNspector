from abc import ABC, abstractmethod

class A(ABC):
    def __init__(self):
        self.a = 1

    @abstractmethod
    def abstract(self):
        pass