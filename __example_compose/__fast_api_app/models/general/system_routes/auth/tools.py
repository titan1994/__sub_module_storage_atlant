from jose import jwt
from passlib.context import CryptContext
from .models import Token

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_access_token(data: dict):
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)  # Генерация токена
    if len(encoded_jwt) > 256:
        encoded_jwt = encoded_jwt[:256]
    await Token.filter(username=data['username']).update(is_active=False)  # Делаем все старые токены неактивными
    token = await Token.create(token=encoded_jwt, username=data['username'])  # генерируем и создаём новый токен
    return token


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)
