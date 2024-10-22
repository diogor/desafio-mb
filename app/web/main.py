from fastapi import FastAPI, HTTPException

from app.core.services import get_symbol_price
from app.web.request import CoinRequest
from app.web.response import CoinResponse

app = FastAPI()


@app.post("/coin_infos", response_model=CoinResponse)
async def coin_infos(coin_request: CoinRequest) -> CoinResponse:
    response = get_symbol_price(coin_request.symbol)

    if not response:
        raise HTTPException(status_code=404, detail="Coin not found")

    return response
