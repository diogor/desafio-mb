from fastapi import FastAPI, HTTPException, status

from app.core.services import get_symbol_price
from app.web.adapters.cache.memory_backend import MemoryBackend
from app.web.request import CoinRequest
from app.web.response import CoinResponse
from app.web.middleware.cache import CacheMiddleware

cache_backend = MemoryBackend()
app = FastAPI()

app.add_middleware(
    CacheMiddleware,
    backend=cache_backend,
    cached_endpoints=["/coin_infos"],
)


@app.post(
    "/coin_infos",
    response_model=CoinResponse,
    responses={400: {"description": "Unknown symbol"}},
)
async def coin_infos(coin_request: CoinRequest) -> CoinResponse:
    response = get_symbol_price(coin_request.symbol)

    if not response:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown symbol"
        )

    return response
