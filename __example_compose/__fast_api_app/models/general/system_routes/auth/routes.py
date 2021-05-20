from typing import Optional

from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .pd import User_Pydantic, UserIn_Pydantic
from .models import User
from .tools import verify_password, get_password_hash, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Security"],
    responses={200: {"message": "Methods for login, registration, authorization"}},
)


@router.post("/registration")
async def reg(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Регистрация: шифруем пароль, создаём пользователя
    """
    username = form_data.username
    password = form_data.password
    if not username or not password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = User_Pydantic(username=username, hashed_password=get_password_hash(password))
    user_db = await User.create(**user.dict())
    return user_db

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Авторизация: проверяем пароль, создаём токен - получаем токен
    """
    username = form_data.username
    password = form_data.password
    if not username or not password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user_db = User.get(username=username)
    user = await User_Pydantic.from_queryset_single(user_db)
    if verify_password(password, user.hashed_password):
        token_model = await create_access_token(user.dict())
        return {"access_token": token_model.token, "token_type": "bearer"}
