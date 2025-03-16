from abc import ABC, abstractmethod


class FileParser(ABC):
    @abstractmethod
    def parse_as_df(self):
        pass


