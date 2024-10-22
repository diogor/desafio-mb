from pydantic import BaseModel


class CoinRequest(BaseModel):
    symbol: str
