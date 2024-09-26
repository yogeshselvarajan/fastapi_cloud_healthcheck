from abc import ABC, abstractmethod
from typing import Dict
from .enums import HealthCheckStatusEnum


class HealthCheckInterface(ABC):
    _identifier: str
    _metadata: Dict[str, str]
    _statusMessages: Dict[str, str]

    @classmethod
    @abstractmethod
    def getMetadata(self) -> Dict[str, str]:
        pass

    @classmethod
    @abstractmethod
    def getStatusMessages(self) -> Dict[str, str]:
        pass

    @classmethod
    @abstractmethod
    def __checkHealth__(self) -> HealthCheckStatusEnum:
        pass
