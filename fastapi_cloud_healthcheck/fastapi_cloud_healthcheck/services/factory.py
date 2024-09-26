from abc import ABC
from ..core.interface import HealthCheckInterface
from ..core.models import HealthCheckModel, HealthCheckEntityModel
from ..core.enums import HealthCheckStatusEnum
from typing import Dict, List
from datetime import datetime


class HealthCheckFactory:
    _healthItems: List[HealthCheckInterface]
    _health: HealthCheckModel

    def __init__(self) -> None:
        self._healthItems = list()

    def add(self, item: HealthCheckInterface) -> None:
        self._healthItems.append(item)

    def __startTimer__(self, entityTimer: bool) -> None:
        if entityTimer:
            self._entityStartTime = datetime.now()
        else:
            self._totalStartTime = datetime.now()

    def __stopTimer__(self, entityTimer: bool) -> None:
        if entityTimer:
            self._entityStopTime = datetime.now()
        else:
            self._totalStopTime = datetime.now()

    def __getTimeTaken__(self, entityTimer: bool) -> datetime:
        if entityTimer:
            return self._entityStopTime - self._entityStartTime
        return self._totalStopTime - self._totalStartTime

    @staticmethod
    def __dump_model__(model: HealthCheckModel) -> dict:
        """Convert Python objects to a JSON-compatible format."""
        entities_list = []
        for entity in model.entities:
            entity_dict = dict(entity)
            entity_dict['healthStatus'] = entity.healthStatus.value
            entity_dict['responseTime'] = str(entity.responseTime) if entity.responseTime else ""
            entities_list.append(entity_dict)

        model_dict = dict(model)
        model_dict['entities'] = entities_list
        model_dict['totalResponseTime'] = str(model.totalResponseTime) if model.totalResponseTime else ""

        return model_dict

    def check(self) -> HealthCheckModel:
        """Run health checks and generate a health report."""
        self._health = HealthCheckModel()
        self.__startTimer__(False)
        unhealthy_found = False

        for item in self._healthItems:
            # Create health check entity model
            entity_item = HealthCheckEntityModel(
                identifier=item._identifier,
                metadata=item.getMetadata(),
                statusMessages=item.getStatusMessages()
            )

            self.__startTimer__(True)
            item_status = item.__checkHealth__()
            self.__stopTimer__(True)

            # Populate response time and status
            entity_item.responseTime = self.__getTimeTaken__(True)
            entity_item.healthStatus = item_status

            # Set status messages
            entity_item.statusMessages = item.getStatusMessages()

            # Update overall health status if any service is unhealthy
            if entity_item.healthStatus == HealthCheckStatusEnum.UNHEALTHY:
                unhealthy_found = True
                entity_item.statusCode = 500
            else:
                entity_item.statusCode = 200

            self._health.entities.append(entity_item)

        self.__stopTimer__(False)
        self._health.totalResponseTime = self.__getTimeTaken__(False)

        # Set overall system health
        if unhealthy_found:
            self._health.systemHealth = {
                "status": "Unhealthy",
                "description": "One or more services are not operating normally.",
                "statusCode": 500,
                "suggestion": "Please investigate the issues."
            }
        else:
            self._health.systemHealth = {
                "status": "Healthy",
                "description": "All services are operating normally.",
                "statusCode": 200,
                "suggestion": "No action needed."
            }

        self._health = self.__dump_model__(self._health)
        return self._health


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
