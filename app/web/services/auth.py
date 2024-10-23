from typing import Annotated, Optional
from fastapi import Depends, HTTPException
from jwt.exceptions import InvalidTokenError
from app.core.exceptions import AlreadyExistsError, AuthenticationError
from app.core.repository import UserRepository
from app.models.auth import TokenData, User
from app.web.adapters.auth.base import Oauth2Base
from app.web.adapters.auth.token_auth import Oauth2TokenAuth, oauth2_scheme


class UserService:
    auth_adapter: Oauth2Base
    user_repository: UserRepository

    def __init__(
        self,
        auth_adapter: Oauth2Base = Oauth2TokenAuth(),
        user_repository: UserRepository = UserRepository(),
    ):
        self.auth_adapter = auth_adapter
        self.user_repository = user_repository

    async def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]):
        try:
            payload = self.auth_adapter.decode_token(token)
            username: str = payload.get("sub", "")
            if not username:
                raise HTTPException(status_code=401, detail="Invalid token")
            token_data = TokenData(username=username)
        except InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = self.user_repository.get_user_by_username(username=token_data.username)
        if user is None:
            raise HTTPException(status_code=401, detail="Authorization failed")
        return user

    def get_user_by_token(self, token: str) -> TokenData:
        try:
            payload = self.auth_adapter.decode_token(token)
            username: str = payload.get("sub", "")
            if not username:
                raise AuthenticationError(message="Invalid token")
            token_data = TokenData(username=username)
        except InvalidTokenError:
            raise AuthenticationError(message="Invalid token")
        return token_data

    def authenticate_user(self, username: str, password: str):
        user = self.user_repository.get_user_by_username(username)
        if not user:
            raise AuthenticationError(message="Invalid credentials")

        if not self.auth_adapter.verify_password(password, user.password):
            raise AuthenticationError(message="Invalid credentials")

        return user

    def create_user(self, username: str, password: str, email: Optional[str]) -> User:
        try:
            user = self.user_repository.create_user(username, password, email)
        except AlreadyExistsError:
            raise AlreadyExistsError(message="User already exists")
        return user
