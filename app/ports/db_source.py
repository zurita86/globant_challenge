from abc import ABC, abstractmethod


class SourceInterface(ABC):

    @abstractmethod
    def query(self, query):
        pass

