import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from app.settings import SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.web.adapters.auth.base import Oauth2Base

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Oauth2TokenAuth(Oauth2Base):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(
        self, plain_password: str | bytes, hashed_password: str | bytes
    ) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str | bytes) -> str:
        return self.pwd_context.hash(password)

    def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)
        return encoded_jwt

    def decode_token(self, token: str) -> dict[str, str]:
        return jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
