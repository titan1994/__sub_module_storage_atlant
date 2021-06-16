from jose import jwt
from passlib.context import CryptContext
from .models import Token
from cryptography.fernet import Fernet
from fastapi import Depends, HTTPException
from MODS.rest_core.pack_core.back_core.FAST_API import oauth2_scheme
from GENERAL_CONFIG import GeneralConfig

ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_access_token(data: dict):
    SECRET_KEY = Fernet.generate_key().decode()
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


if getattr(GeneralConfig, 'SECRET_KEY', None):
    async def verify_token(token=Depends(oauth2_scheme)):
        token_db = await Token.filter(token=token).first()
        if token_db:
            if token_db.is_active:
                return True
        raise HTTPException(status_code=403, detail='Bad token')
else:
    async def verify_token(token=Depends(None)):
        pass

