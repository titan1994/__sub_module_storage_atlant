"""
Универсальное API для работы с моделями
"""

from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from tortoise.contrib.pydantic import pydantic_model_creator


from MODS.standart_namespace.routes import standardize_response
from .tools.get_class import get_orm_class
from .tools.create_model import create_some


router = APIRouter(
    prefix="/orm",
    tags=["ORM-Dictionaries"],
    responses={404: {"description": "Not found"}},
)


class ORMProcessingError(Exception):
    pass


@router.get("/{client_key}/{dict_name}")
@standardize_response
async def orm_get_model_list(client_key: str, dict_name: str):
    """
    Универсальное получение списка
    """
    class_model = get_orm_class(client_key=client_key, dict_name=dict_name)
    if not class_model:
        raise ORMProcessingError('Model not found!')

    pyd_model = pydantic_model_creator(class_model)
    model_list = await pyd_model.from_queryset(class_model.all())
    if not model_list:
        raise ORMProcessingError('Model list is empty!')

    res = jsonable_encoder(model_list)
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
