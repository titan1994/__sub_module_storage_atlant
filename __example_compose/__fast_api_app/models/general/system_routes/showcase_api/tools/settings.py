from MODS.storage_atlant_driver.pack_core.psql_jsonb.connector import get_client
from MODS.storage_atlant_driver.pack_core.main import DEFAULT_META_NAME_SHOWCASE
from fastapi import HTTPException


async def get_showcase_data(client_key, showcase_name):
    """
    Получение данных витрины из хранилища метаданных
    """

    client_data = await get_client(client_key=client_key)
    try:
        showcase_data = client_data[0]['structureBody'][DEFAULT_META_NAME_SHOWCASE][showcase_name]
    except Exception as exp:
        raise Exception("Client or showcase not found")

    return showcase_data
