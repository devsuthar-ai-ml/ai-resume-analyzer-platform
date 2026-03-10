import time
from collections import defaultdict

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import get_settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.request_log = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/docs") or request.url.path.startswith("/openapi"):
            return await call_next(request)

        settings = get_settings()
        now = time.time()
        ip = request.client.host if request.client else "unknown"
        window = settings.rate_limit_window_seconds
        limit = settings.rate_limit_requests

        recent = [ts for ts in self.request_log[ip] if now - ts < window]
        self.request_log[ip] = recent

        if len(recent) >= limit:
            return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded. Try again later."})

        self.request_log[ip].append(now)
        return await call_next(request)
