"""
Универсальное API для работы с моделями
"""

from json import load as jsf
from fastapi import APIRouter, Body, Depends

from MODS.scripts.python.easy_scripts import PROJECT_GENERAL_FOLDER
from MODS.standart_namespace.routes import standardize_response

from MODS.storage_atlant_driver.pack_core.SHOWCASE.constructor import \
    smart_create_showcases, smart_delete_showcases
from ...system_routes.auth.tools import verify_token

router = APIRouter(
    prefix="/settings",
    tags=["SETTINGS. Showcase"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(verify_token)]
)

"""
Примеры
"""

try:
    DEFAULT_PATH_EXAMPLE_POST_DATA = PROJECT_GENERAL_FOLDER / '__test_data' / 'showcase' / '__post_add_or_update.json'
    with open(DEFAULT_PATH_EXAMPLE_POST_DATA, 'r', encoding='utf8') as fobj:
        EXAMPLE_POST_CLIENT_DATA = jsf(fobj)

    DEFAULT_PATH_EXAMPLE_DELETE = PROJECT_GENERAL_FOLDER / '__test_data' / 'showcase' / '__delete.json'
    with open(DEFAULT_PATH_EXAMPLE_DELETE, 'r', encoding='utf8') as fobj:
        EXAMPLE_DELETE_CLIENT_DATA = jsf(fobj)

except FileNotFoundError:
    EXAMPLE_POST_CLIENT_DATA = None
    EXAMPLE_DELETE_CLIENT_DATA = None

"""
Создание
"""


@router.post("/showcase")
@standardize_response
async def settings_showcase_create(body=Body(..., example=EXAMPLE_POST_CLIENT_DATA)):
    """
    Создание НСИ
    """

    res = await smart_create_showcases(json_data=body)
    return res


"""
Удаление
"""


@router.delete("/showcase")
@standardize_response
async def settings_showcase_delete(body=Body(..., example=EXAMPLE_DELETE_CLIENT_DATA)):
    """
    Удаление НСИ
    """

    res = await smart_delete_showcases(json_data=body)
    return res
