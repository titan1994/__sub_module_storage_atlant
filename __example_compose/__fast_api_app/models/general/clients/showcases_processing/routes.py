"""
Универсальное API для работы с моделями
"""
from pathlib import Path
import importlib.util


from fastapi import APIRouter, Body
from MODS.standart_namespace.routes import standardize_response
from MODS.scripts.python.easy_scripts import get_module_name
from MODS.storage_atlant_driver.pack_core.psql_jsonb.connector import get_client

from MODS.storage_atlant_driver.pack_core.main import DEFAULT_META_NAME_SHOWCASE

DEFAULT_PROC_NAME_FILE = 'processor.py'

router = APIRouter(
    prefix="/showcases/clients_data",
    tags=["CLIENTS-API"],
    responses={404: {"description": "Not found"}},
)


class ClientProcessorNotFound(Exception):
    pass


@router.post("/{client_key}/{showcase_name}")
@standardize_response
async def post_client_data_to_showcase(client_key: str, showcase_name: str, body=Body(...)):
    """
    Свитчер обработчиков данных от клиентов
    """

    mod = get_client_module(client_key=client_key)

    client_data = await get_client(client_key=client_key)

    try:
        showcase = client_data[0]['structureBody'][DEFAULT_META_NAME_SHOWCASE][showcase_name]
    except Exception as exp:
        raise ClientProcessorNotFound(f'showcase {showcase_name} is not settings!')

    result = await mod.process_input_data(
        client_key = client_key,
        showcase = showcase,
        showcase_name = showcase_name,
        json_in=body
    )

    return result


def get_client_module(client_key):
    """
    Поиск модуля обработчика для клиента
    """
    folder_processing = Path(__file__).parent / client_key
    if not folder_processing.exists():
        raise ClientProcessorNotFound(f'{client_key} processor folder not found!')

    path_to_module = folder_processing / DEFAULT_PROC_NAME_FILE
    spec = importlib.util.spec_from_file_location(f'{path_to_module.stem}', path_to_module)

    # creating a new module based on spec
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    return mod
