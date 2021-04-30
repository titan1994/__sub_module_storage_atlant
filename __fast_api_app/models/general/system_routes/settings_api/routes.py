"""
Универсальное API для работы с моделями
"""

from fastapi import APIRouter, Body
from MODS.standart_namespace.routes import standardize_response

router = APIRouter(
    prefix="/settings",
    tags=["ORM-Dictionaries"],
    responses={404: {"description": "Not found"}},
)


@router.post("/client")
@standardize_response
async def orm_get_model_list():
    """
    Создание клиента
    """

