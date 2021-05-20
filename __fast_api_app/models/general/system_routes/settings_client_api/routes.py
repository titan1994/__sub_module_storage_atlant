"""
Универсальное API для работы с моделями
"""
from json import load as jsf
from typing import Optional

from fastapi import APIRouter, Body
from MODS.scripts.python.easy_scripts import PROJECT_GENERAL_FOLDER
from MODS.standart_namespace.routes import standardize_response
from MODS.storage_atlant_driver.pack_core.HEART.client_api import \
    smart_create_client, smart_delete_client

from .tools.get_list import get_meta_clients

router = APIRouter(
    prefix="/settings",
    tags=["SETTINGS. Client"],
    responses={404: {"description": "Not found"}},
)

"""
Примеры
"""

try:
    DEFAULT_PATH_EXAMPLE_POST_DATA = PROJECT_GENERAL_FOLDER / '__test_data' / 'client' / '__post_add_or_update..json'
    with open(DEFAULT_PATH_EXAMPLE_POST_DATA, 'r', encoding='utf8') as fobj:
        EXAMPLE_POST_CLIENT_DATA = jsf(fobj)

    DEFAULT_PATH_EXAMPLE_DELETE = PROJECT_GENERAL_FOLDER / '__test_data' / 'client' / '__delete.json'
    with open(DEFAULT_PATH_EXAMPLE_DELETE, 'r', encoding='utf8') as fobj:
        EXAMPLE_DELETE_CLIENT_DATA = jsf(fobj)

except FileNotFoundError:
    EXAMPLE_POST_CLIENT_DATA = None
    EXAMPLE_DELETE_CLIENT_DATA = None

"""
Получение клиентов
"""


@router.get("/client")
@standardize_response
async def settings_client_get_all(client_key: Optional[str] = None):
    """
    Информация по клиенту. Если не указан - то по всем клиентам
    """

    res = await get_meta_clients(client_key=client_key)
    return res


"""
Создание клиентов
"""


@router.post("/client")
@standardize_response
async def settings_client_create(body=Body(..., example=EXAMPLE_POST_CLIENT_DATA)):
    """
    Создание клиента
    """

    res = await smart_create_client(json_data=body)
    return res


"""
Удаление клиентов
"""


@router.delete("/client")
@standardize_response
async def settings_client_delete(body=Body(..., example=EXAMPLE_DELETE_CLIENT_DATA)):
    """
    Удаление клиента
    """

    res = await smart_delete_client(json_data=body)
    return res
