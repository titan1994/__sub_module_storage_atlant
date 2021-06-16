"""
Универсальное API для работы с моделями
"""
from pathlib import Path
import importlib.util
from typing import Optional
from json import loads as jsl

from fastapi import APIRouter, Body, Depends, File, UploadFile
from MODS.standart_namespace.routes import standardize_response
from MODS.storage_atlant_driver.pack_core.psql_jsonb.connector import get_client
from __fast_api_app.models.general.system_routes.auth.tools import verify_token

from MODS.storage_atlant_driver.pack_core.main import \
    DEFAULT_META_NAME_SHOWCASE, \
    gen_showcase_table_name_showcase

"""
Конфиг
"""

from GENERAL_CONFIG import GeneralConfig

DEFAULT_PROC_CONFIGURE = {
    'POST_DATA': ['input_data.py', 'client_post_processing_data'],
    'GET_DATA': ['output_data.py', 'client_get_data']
}

router = APIRouter(
    prefix="/showcases/clients-data",
    tags=["INDIVIDUAL-API"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(verify_token)]
)


class ClientProcessorNotFound(Exception):
    pass


"""
Свитчеры индивидуальных обработчиков
"""


@router.post("/individual-input/{client_key}/{showcase_name}")
@standardize_response
async def ind_post_client_data_from_body_to_showcase(client_key: str, showcase_name: str, body=Body(...)):
    """
    Индивидуальная вставка данных в витрину - через тело запроса
    """

    result = await ind_post_client_data_to_showcase(
        client_key=client_key,
        showcase_name=showcase_name,
        json_in=body
    )

    return result


@router.post("/individual-input/{client_key}/{showcase_name}/file")
@standardize_response
async def ind_post_client_data_from_file_to_showcase(client_key: str, showcase_name: str, file: bytes = File(...)):
    """
    Индивидуальная вставка данных в витрину - через файл json
    """

    json_in = jsl(file)
    result = await ind_post_client_data_to_showcase(
        client_key=client_key,
        showcase_name=showcase_name,
        json_in=json_in
    )

    return result


@router.post("/individual-input/{client_key}/{showcase_name}/long_file")
@standardize_response
async def ind_post_client_data_from_long_file_to_showcase(client_key: str, showcase_name: str,
                                                          file: UploadFile = File(...)):
    """
    Индивидуальная вставка данных в витрину - через файл размером больше 5 Мб
    """

    result = await ind_post_client_data_to_showcase(
        client_key=client_key,
        showcase_name=showcase_name,
        json_in=file
    )

    return result


async def ind_post_client_data_to_showcase(client_key, showcase_name, json_in):
    """
    Индивидуальная вставка данных в витрину - обобщение
    """

    func = get_processing_func(
        client_key=client_key,
        proc_name='POST_DATA'
    )

    showcase_data = await get_showcase_data(
        client_key=client_key,
        showcase_name=showcase_name
    )

    result = await func(
        client_key=client_key,
        showcase=showcase_data,
        showcase_name=showcase_name,
        json_in=json_in
    )

    return result


@router.post("/individual-output/{client_key}/{showcase_name}")
@standardize_response
async def ind_get_client_data_from_showcase(client_key: str, showcase_name: str, body: Optional[dict] = None):
    """
    Индивидуальное получение данных витрины
    """

    func = get_processing_func(
        client_key=client_key,
        proc_name='GET_DATA'
    )

    name_table = gen_showcase_table_name_showcase(
        client_key=client_key,
        name_showcase=showcase_name
    )

    if not body:
        body = {}

    result = await func(
        client_key=client_key,
        showcase_name=showcase_name,
        table_name=name_table,
        json_in=body
    )

    return result


"""
Универсальные/базовые обработчики данных
"""

"""
Обобщённый функционал
"""


async def get_showcase_data(client_key, showcase_name):
    """
    Получение данных витрины из хранилища метаданных
    """

    client_data = await get_client(client_key=client_key)
    try:
        showcase_data = client_data[0]['structureBody'][DEFAULT_META_NAME_SHOWCASE][showcase_name]
    except Exception as exp:
        raise ClientProcessorNotFound(f'showcase {showcase_name} is not settings!')

    return showcase_data


def get_processing_func(client_key, proc_name):
    """
    Получение функции обработчика для клиента
    """

    mod = get_client_module(client_key=client_key, module_name=DEFAULT_PROC_CONFIGURE[proc_name][0])
    func = getattr(mod, DEFAULT_PROC_CONFIGURE[proc_name][1], None)
    if not func:
        raise ClientProcessorNotFound(f'client {client_key} processor is not settings!')

    return func


def get_client_module(client_key, module_name):
    """
    Поиск модуля обработчика для клиента
    """
    folder_processing = Path(GeneralConfig.ATLANT_STORAGE_INDIVIDUAL_API_FOLDER) / client_key
    if not folder_processing.exists():
        raise ClientProcessorNotFound(f'{client_key} processor folder not found!')

    path_to_module = folder_processing / module_name
    spec = importlib.util.spec_from_file_location(f'{path_to_module.stem}', path_to_module)

    # creating a new module based on spec
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    return mod
