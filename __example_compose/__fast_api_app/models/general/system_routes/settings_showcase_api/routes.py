"""
Универсальное API для работы с моделями
"""

from fastapi import APIRouter, Body
from MODS.standart_namespace.routes import standardize_response

from MODS.storage_atlant_driver.pack_core.SHOWCASE.constructor import \
    smart_create_showcases, smart_delete_showcases

router = APIRouter(
    prefix="/settings",
    tags=["SETTINGS. Showcase"],
    responses={404: {"description": "Not found"}},
)


@router.post("/showcase")
@standardize_response
async def settings_showcase_create(body=Body(...)):
    """
    Создание НСИ
    """

    res = await smart_create_showcases(json_data=body)
    return res


@router.delete("/showcase")
@standardize_response
async def settings_showcase_delete(body=Body(...)):
    """
    Удаление НСИ
    """

    res = await smart_delete_showcases(json_data=body)
    return res
