from fastapi import APIRouter, Body, Depends, File, UploadFile
from fastapi_pagination import Params, paginate
from MODS.standart_namespace.routes import standardize_response
from .tools.select import showcase_select_base, showcase_select_union, EXAMPLE_SELECT_BASE, EXAMPLE_SELECT_UNION
from .tools.insert import showcase_insert_universal, INSERT_EXAMPLE
from json import loads as jsl
import ijson

router = APIRouter(
    prefix="/showcases-api/clients-data",
    tags=["CLIENTS-API"],
    responses={404: {"description": "Not found"}},
)


@router.post("/select-base/{client_key}/{showcase_name}/")
@standardize_response
async def select_base_route(
        client_key: str,
        showcase_name: str,
        body=Body(..., example=EXAMPLE_SELECT_BASE),
        params: Params = Depends(),
        pagination: bool = True
):
    """
    Универсальный маршрут для отправки select запроса к витрине
    """
    result = await showcase_select_base(client_key, showcase_name, body)
    if pagination:
        page = paginate(result, params).json()
        return page
    return result


@router.post("/select-union/{client_key}/")
@standardize_response
async def select_union_route(
        client_key: str,
        body=Body(..., example=EXAMPLE_SELECT_UNION),
        params: Params = Depends(),
        pagination: bool = True
):
    """
    Универсальный маршрут для отправки объединённых select запросов к витрине
    """
    result = await showcase_select_union(client_key, body)
    if pagination:
        page = paginate(result, params).json()
        return page
    return result


@router.post("/insert-universal/{client}/{showcase}/file/small/")
@standardize_response
async def insert_route(
        client: str, showcase: str,
        body: bytes = File(...),
        auto_flushing: int = 10000,
        use_tx: bool = False,
        kafka_key: str = None):
    """
    Универсальный маршрут для вставки данных в витрину
    """
    body = jsl(body)
    result = await showcase_insert_universal(client, showcase, body, auto_flushing, use_tx, kafka_key)
    return result


@router.post("/insert-universal/{client}/{showcase}/file/long/")
@standardize_response
async def insert_route(
        client: str, showcase,
        file: UploadFile = File(...),
        auto_flushing: int = 10000,
        use_tx: bool = False,
        kafka_key: str = None):
    """
    Универсальный маршрут для вставки данных в витрину
    """
    json_async = ijson.items(file, 'item')
    result = await showcase_insert_universal(client, showcase, json_async, auto_flushing, use_tx, kafka_key, True)
    return result


@router.post("/insert-universal/{client}/{showcase}/json/body/")
@standardize_response
async def insert_route(
        client: str, showcase,
        body=Body(..., example=INSERT_EXAMPLE),
        auto_flushing: int = 10000,
        use_tx: bool = False,
        kafka_key: str = None):
    """
    Универсальный маршрут для вставки данных в витрину
    """
    result = await showcase_insert_universal(client, showcase, body, auto_flushing, use_tx, kafka_key)
    return result
