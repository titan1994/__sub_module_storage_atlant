"""
Универсальное API для работы с моделями
"""

from fastapi import APIRouter, Body
from MODS.standart_namespace.routes import standardize_response
from MODS.storage_atlant_driver.pack_core.HEART.client_api import \
    smart_create_client, smart_delete_client

from .tools.get_list import get_meta_clients

router = APIRouter(
    prefix="/settings",
    tags=["SETTINGS. Client"],
    responses={404: {"description": "Not found"}},
)


@router.post("/client")
@standardize_response
async def settings_client_create(body=Body(...)):
    """
    Создание клиента
    """

    res = await smart_create_client(json_data=body)
    return res


@router.delete("/client")
@standardize_response
async def settings_client_delete(body=Body(...)):
    """
    Удаление клиента
    """

    res = await smart_delete_client(json_data=body)
    return res


@router.get("/client")
@standardize_response
async def settings_client_get_all():
    """
    Список всех клиентов. Их конфигурации
    """

    res = await get_meta_clients()
    return res
