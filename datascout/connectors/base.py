from abc import ABC, abstractmethod
from typing import List
from datascout.models import DatasetRecord

class BaseConnector(ABC):
    source_name: str = "base"
    @abstractmethod
    async def search(self, query: str, limit: int = 10) -> List[DatasetRecord]:
        pass