"""
Универсальное API для работы с моделями
"""

from fastapi import APIRouter, Body
from MODS.standart_namespace.routes import standardize_response



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
    pass

