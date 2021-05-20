"""
Универсальное API для работы с моделями
"""

from json import load as jsf
from fastapi import APIRouter, Body

from MODS.scripts.python.easy_scripts import PROJECT_GENERAL_FOLDER
from MODS.standart_namespace.routes import standardize_response
from MODS.storage_atlant_driver.pack_core.NSI.tortoise_bridge import \
    bridge_smart_create_dictionaries, bridge_smart_delete_dictionaries

router = APIRouter(
    prefix="/settings",
    tags=["SETTINGS. Dictionaries"],
    responses={404: {"description": "Not found"}},
)

"""
Примеры 
"""

DEFAULT_PATH_EXAMPLE_POST_DATA = PROJECT_GENERAL_FOLDER / '__test_data' / 'dictionary' / '__post_add_or_update.json'
with open(DEFAULT_PATH_EXAMPLE_POST_DATA, 'r', encoding='utf8') as fobj:
    EXAMPLE_POST_CLIENT_DATA = jsf(fobj)

DEFAULT_PATH_EXAMPLE_DELETE = PROJECT_GENERAL_FOLDER / '__test_data' / 'dictionary' / '__delete.json'
with open(DEFAULT_PATH_EXAMPLE_DELETE, 'r', encoding='utf8') as fobj:
    EXAMPLE_DELETE_CLIENT_DATA = jsf(fobj)

"""
Создание
"""


@router.post("/dictionary")
@standardize_response
async def settings_dict_create(body=Body(..., example=EXAMPLE_POST_CLIENT_DATA)):
    """
    Создание НСИ
    """

    res = await bridge_smart_create_dictionaries(data_json=body)
    return res


"""
Удаление
"""


@router.delete("/dictionary")
@standardize_response
async def settings_dict_delete(body=Body(..., example=EXAMPLE_DELETE_CLIENT_DATA)):
    """
    Удаление НСИ
    """

    res = await bridge_smart_delete_dictionaries(data_json=body)
    return res
