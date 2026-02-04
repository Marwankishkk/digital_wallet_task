from abc import ABC, abstractmethod
from models.transaction import Transaction

class BaseBankParser(ABC):

    @abstractmethod
    def parse(self, line: str) -> Transaction:
        """
        Takes a single transaction line from a bank webhook
        and returns a normalized Transaction object.
        """
        pass
