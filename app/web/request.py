from pydantic import BaseModel


class CoinRequest(BaseModel):
    symbol: str


class CreateUserRequest(BaseModel):
    username: str
    password: str
    email: str | None = None
