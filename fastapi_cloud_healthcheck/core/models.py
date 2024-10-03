from datetime import timedelta
from typing import List, Dict, Optional, Union
from pydantic import BaseModel, Field, field_validator
from .enums import HealthCheckStatusEnum


class SystemHealthModel(BaseModel):
    status: Union[HealthCheckStatusEnum, str] = HealthCheckStatusEnum.HEALTHY
    description: str = "All services are operating normally."
    statusCode: int = 200
    suggestion: str = "No action needed."


class HealthCheckSummaryModel(BaseModel):
    totalServices: int = 0
    healthyServices: int = 0
    unhealthyServices: int = 0
    warningServices: int = 0


class HealthCheckEntityModel(BaseModel):
    identifier: str
    healthStatus: Union[HealthCheckStatusEnum, str] = HealthCheckStatusEnum.HEALTHY
    statusCode: int = 200
    responseTime: Optional[timedelta] = None
    metadata: Dict[str, str] = Field(default_factory=dict)
    statusMessages: Dict[str, str] = Field(default_factory=dict)


class HealthCheckModel(BaseModel):
    systemHealth: Union[SystemHealthModel, Dict[str, Union[str, int]]] = SystemHealthModel()
    totalResponseTime: Optional[timedelta] = None
    lastUpdated: Optional[str] = ""
    summary: HealthCheckSummaryModel = HealthCheckSummaryModel()
    entities: List[HealthCheckEntityModel] = Field(default_factory=list)
