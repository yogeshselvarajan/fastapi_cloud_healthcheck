from enum import Enum


class HealthCheckStatusEnum(Enum):
    HEALTHY = "Healthy"
    WARNING = "Warning"
    UNHEALTHY = "Unhealthy"
