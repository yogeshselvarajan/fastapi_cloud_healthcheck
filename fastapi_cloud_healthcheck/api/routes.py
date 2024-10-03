from typing import Callable
from starlette.responses import JSONResponse
from ..services.factory import HealthCheckFactory
from ..core.enums import HealthCheckStatusEnum


def create_health_check_route(factory: HealthCheckFactory) -> Callable:
    _factory = factory

    def endpoint() -> JSONResponse:
        # Perform the health check and get the report
        health_report = _factory.check()

        # Determine the system health status and set the appropriate HTTP status code
        system_health_status = health_report['systemHealth']['status']

        if system_health_status == HealthCheckStatusEnum.UNHEALTHY.value:
            return JSONResponse(content=health_report, status_code=500)

        elif system_health_status == HealthCheckStatusEnum.WARNING.value:
            return JSONResponse(content=health_report, status_code=300)

        return JSONResponse(content=health_report, status_code=200)

    return endpoint

