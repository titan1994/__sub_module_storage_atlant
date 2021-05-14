"""
Универсальное API для работы с моделями
"""

from fastapi import APIRouter, Body
from MODS.standart_namespace.routes import standardize_response
from MODS.storage_atlant_driver.pack_core.NSI.tortoise_bridge import \
    bridge_smart_create_dictionaries, bridge_smart_delete_dictionaries

router = APIRouter(
    prefix="/settings",
    tags=["SETTINGS. Dictionaries"],
    responses={404: {"description": "Not found"}},
)


@router.post("/dictionary")
@standardize_response
async def settings_dict_create(body=Body(...)):
    """
    Создание НСИ
    """

    res = await bridge_smart_create_dictionaries(data_json=body)
    from tortoise import Tortoise
    
    from MODS.rest_core.pack_core.aerich_proc import config as cfg_tortoise
    await Tortoise.init(config=cfg_tortoise.get_tortoise_config())

    return res


@router.delete("/dictionary")
@standardize_response
async def settings_dict_delete(body=Body(...)):
    """
    Удаление НСИ
    """

    res = await bridge_smart_delete_dictionaries(data_json=body)
    return res
