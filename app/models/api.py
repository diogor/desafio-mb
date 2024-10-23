from pydantic import BaseModel


class APIInfo(BaseModel):
    id: str
    name: str
    uri: str
    coin_name: str | None
    symbol: str | None
    coin_price: str
