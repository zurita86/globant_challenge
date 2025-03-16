from abc import ABC, abstractmethod


class DestinationInterface(ABC):
    @abstractmethod
    def load_table(self, df, table_id):
        pass

    @abstractmethod
    def get_table(self, table_id):
        pass

