from datetime import datetime
from typing import List, Dict, Optional, Union
from pydantic import BaseModel
from .enums import HealthCheckStatusEnum


class HealthCheckEntityModel(BaseModel):
    identifier: str
    healthStatus: Union[HealthCheckStatusEnum, str] = HealthCheckStatusEnum.HEALTHY
    statusCode: int = 200
    responseTime: Union[Optional[str], str] = ""
    metadata: Dict[str, Union[str, datetime]] = dict()
    statusMessages: Dict[str, str] = dict()


class SystemHealthModel(BaseModel):
    status: Union[HealthCheckStatusEnum, str] = HealthCheckStatusEnum.HEALTHY
    description: str = "All services are operating normally."
    statusCode: int = 200
    suggestion: str = "No action needed."


class HealthCheckModel(BaseModel):
    systemHealth: SystemHealthModel = SystemHealthModel()
    totalResponseTime: Union[Optional[str], str] = ""
    entities: List[HealthCheckEntityModel] = list()
