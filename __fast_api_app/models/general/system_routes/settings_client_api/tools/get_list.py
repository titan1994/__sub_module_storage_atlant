"""
Получение списка клиентов
"""

from MODS.storage_atlant_driver.pack_core.psql_jsonb.connector import \
    get_all_clients, get_key_app, \
    DEFAULT_client_key_NAME


async def get_meta_clients(**kwargs):
    """
    Все метаданные клиентов приложения
    """

    list_objs = await get_all_clients()

    summary_result = {}
    for obj_meta in list_objs:
        data_obj = obj_meta.get('structureBody')
        meta_info = obj_meta.get('structureMetadata', {}).get(get_key_app(DEFAULT_client_key_NAME))
        if data_obj and meta_info:
            summary_result[meta_info] = data_obj

    return summary_result
