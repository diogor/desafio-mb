from typing import List

from fastapi import Request
from starlette.concurrency import iterate_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse, Response

from app.web.adapters.cache.backend import BaseBackend
from app.settings import CACHE_SECONDS


class CacheMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        cached_endpoints: List[str],
        backend: BaseBackend,
        cache_seconds: int = CACHE_SECONDS,
        cached_methods: List[str] = ["GET", "POST"],
    ):
        super().__init__(app)
        self.cached_endpoints = cached_endpoints
        self.backend = backend
        self.cache_seconds = cache_seconds
        self.cached_methods = cached_methods

    def matches_any_path(self, path_url):
        for pattern in self.cached_endpoints:
            if pattern in path_url:
                return True
        return False

    async def dispatch(self, request: Request, call_next) -> Response:
        path_url = request.url.path
        request_type = request.method
        auth = request.headers.get("Authorization", "Bearer public")
        token = auth.split(" ")[1]
        body = await request.json()

        key = f"{path_url}_{token}_{body.get('symbol', '')}"

        matches = self.matches_any_path(path_url)
        if not matches or request_type not in self.cached_methods:
            return await call_next(request)

        res = await self.backend.retrieve(key)
        if not res:
            response: Response = await call_next(request)
            response_body = [chunk async for chunk in response.body_iterator]
            response.body_iterator = iterate_in_threadpool(iter(response_body))

            if response.status_code == 200:
                await self.backend.create(
                    response_body[0].decode(), key, self.cache_seconds
                )
            return response

        else:
            # If the response is cached, return it directly
            json_data_str = res[0].decode("utf-8")
            return StreamingResponse(
                iter([json_data_str]), media_type="application/json"
            )
