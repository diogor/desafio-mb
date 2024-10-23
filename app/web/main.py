from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.exceptions import AlreadyExistsError, AuthenticationError
from app.core.api import get_symbol_price
from app.web.adapters.cache.memory_backend import MemoryBackend
from app.web.request import CoinRequest, CreateUserRequest
from app.web.response import CoinResponse, UserResponse
from app.web.middleware.cache import CacheMiddleware
from app.models.auth import Token, User
from app.web.services.auth import UserService
from app.web.adapters.auth.token_auth import Oauth2TokenAuth

cache_backend = MemoryBackend()
app = FastAPI()

app.add_middleware(
    CacheMiddleware,
    backend=cache_backend,
    cached_endpoints=["/coin_infos"],
)

auth_adapter = Oauth2TokenAuth()
user_service = UserService()


@app.post(
    "/coin_infos",
    response_model=CoinResponse,
    responses={400: {"description": "Unknown symbol"}},
)
async def coin_infos(
    coin_request: CoinRequest,
    _: Annotated[User, Depends(user_service.get_current_user)],
) -> CoinResponse:
    response = get_symbol_price(coin_request.symbol)

    if not response:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown symbol"
        )

    return response


@app.post("/token")
async def get_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    try:
        user = user_service.authenticate_user(form_data.username, form_data.password)
    except AuthenticationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = auth_adapter.create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


@app.post("/users/", response_model=UserResponse)
async def create_user(request: CreateUserRequest) -> UserResponse:
    try:
        user = user_service.create_user(
            request.username, request.password, request.email
        )
    except AlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
    )
