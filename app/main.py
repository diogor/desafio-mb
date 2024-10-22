from fastapi import FastAPI

from app.request import CoinRequest
from app.response import CoinResponse

app = FastAPI()


@app.post("/coin_infos", response_model=CoinResponse)
async def coin_infos(coin_request: CoinRequest) -> CoinResponse:
    return {}
