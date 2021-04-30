"""
Универсальное API для работы с моделями
"""

from fastapi import APIRouter, Body

from MODS.standart_namespace.routes import standardize_response
from .tools.create_model import create_some
from .tools.get_model import get_some

router = APIRouter(
    prefix="/orm",
    tags=["ORM-Dictionaries"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{client_key}/{dict_name}")
@standardize_response
async def orm_get_model_list(client_key: str, dict_name: str):
    """
    Универсальное получение списка
    """
    res = await get_some(
        client_key=client_key,
        dict_name=dict_name,
    )

    return res


@router.post("/{client_key}/{dict_name}")
@standardize_response
async def orm_post_model_list(client_key: str, dict_name: str, body=Body(...)):
    """
    Универсальная вставка модели
    """

    res = await create_some(
        client_key=client_key,
        dict_name=dict_name,
        body=body
    )

    return res
