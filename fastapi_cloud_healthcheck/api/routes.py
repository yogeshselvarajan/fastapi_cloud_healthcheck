from typing import Callable
from starlette.responses import JSONResponse
from ..services.factory import HealthCheckFactory
from ..core.enums import HealthCheckStatusEnum


def create_health_check_route(factory: HealthCheckFactory) -> Callable:
    _factory = factory

    def endpoint() -> JSONResponse:
        # Perform the health check and get the report
        res = _factory.check()

        # Determine the system health status and set the appropriate HTTP status code
        if res['systemHealth']['status'] == HealthCheckStatusEnum.UNHEALTHY.value:
            return JSONResponse(content=res, status_code=500)

        # If the overall health is healthy, return with status code 200
        return JSONResponse(content=res, status_code=200)

    return endpoint

