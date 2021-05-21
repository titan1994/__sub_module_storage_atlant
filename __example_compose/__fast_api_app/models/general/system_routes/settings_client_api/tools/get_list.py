"""
Получение списка клиентов
"""

from MODS.storage_atlant_driver.pack_core.psql_jsonb.connector import \
    get_all_clients, \
    get_client, \
    get_key_app, \
    DEFAULT_client_key_NAME


class ClientProcessingError(Exception):
    pass


async def get_meta_clients(client_key=None):
    """
    Все метаданные клиентов приложения
    """

    if client_key:
        list_objs = await get_client(client_key=client_key)
        if not list_objs:
            raise ClientProcessingError(f'Client {client_key} not found!')
    else:
        list_objs = await get_all_clients()
        if not list_objs:
            raise ClientProcessingError('Clients is empty!')

    summary_result = {}
    for obj_meta in list_objs:
        data_obj = obj_meta.get('structureBody')
        meta_info = obj_meta.get('structureMetadata', {}).get(get_key_app(DEFAULT_client_key_NAME))
        if data_obj and meta_info:
            summary_result[meta_info] = data_obj

    return summary_result
