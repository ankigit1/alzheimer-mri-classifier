import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from logger import get_logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.logger = get_logger("requests", "inference.log")

    async def dispatch(self, request: Request, call_next):
        request_id = uuid.uuid4().hex
        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception as exc:
            duration_ms = (time.perf_counter() - start) * 1000
            self.logger.exception(
                "%s %s failed in %.2fms",
                request.method,
                request.url.path,
                duration_ms,
                extra={"request_id": request_id},
            )
            raise exc

        duration_ms = (time.perf_counter() - start) * 1000
        client_host = request.client.host if request.client else "-"
        self.logger.info(
            "%s %s %s %.2fms client=%s",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
            client_host,
            extra={"request_id": request_id},
        )
        response.headers["X-Request-ID"] = request_id
        return response
