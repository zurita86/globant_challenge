from abc import ABC, abstractmethod


class DestinationInterface(ABC):
    @abstractmethod
    def load_table(self, df):
        pass

    @abstractmethod
    def get_table(self):
        pass

