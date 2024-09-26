from typing import Dict
from ..core.interface import HealthCheckInterface
from abc import ABC


class HealthCheckBase(HealthCheckInterface, ABC):
    """Base class for implementing health checks for specific services."""

    def __init__(self):
        self._statusMessages = {}

    def getMetadata(self) -> Dict[str, str]:
        """Return metadata for the service."""
        return self._metadata

    def getStatusMessages(self) -> Dict[str, str]:
        """Return status messages related to the health checks."""
        return self._statusMessages
