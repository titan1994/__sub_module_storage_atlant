from fastapi import APIRouter, Body, Depends, File, UploadFile
from fastapi_pagination import Params, paginate

from MODS.standart_namespace.routes import standardize_response

from .tools.select import showcase_select_base, showcase_select_union, EXAMPLE_SELECT_BASE, EXAMPLE_SELECT_UNION
from .tools.insert import showcase_insert_universal, INSERT_EXAMPLE
from .tools.input_formats import FormatTypes
from .tools.BaseInsert import InsertBodyJson, InsertFileLarge, InsertFileSmall

DEFAULT_KAFKA_BATCH_FLUSH = 10000
DEFAULT_KAFKA_USE_TX = False
DEFAULT_KAFKA_DATA_KEY = None

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


@router.post("/insert-universal/{client}/{showcase}/file-small/json/")
@standardize_response
async def insert_route(
        client: str, showcase: str,
        file: bytes = File(...),
        auto_flushing: int = DEFAULT_KAFKA_BATCH_FLUSH,
        use_tx: bool = DEFAULT_KAFKA_USE_TX,
        kafka_key: str = DEFAULT_KAFKA_DATA_KEY):
    """
    Универсальный маршрут для вставки данных в витрину
    """

    result = await InsertFileSmall(
        client,
        showcase,
        file,
        auto_flushing,
        use_tx,
        kafka_key
    ).insert()
    return result


@router.post("/insert-universal/{client}/{showcase}/file-long/json/")
@standardize_response
async def insert_route(
        client: str, showcase,
        file: UploadFile = File(...),
        auto_flushing: int = DEFAULT_KAFKA_BATCH_FLUSH,
        use_tx: bool = DEFAULT_KAFKA_USE_TX,
        kafka_key: str = DEFAULT_KAFKA_DATA_KEY):
    """
    Универсальный маршрут для вставки данных в витрину
    """

    result = await InsertFileLarge(
        client,
        showcase,
        file,
        auto_flushing,
        use_tx,
        kafka_key
    ).insert()
    return result


@router.post("/insert-universal/{client}/{showcase}/body/json/")
@standardize_response
async def insert_route(
        client: str, showcase,
        body=Body(..., example=INSERT_EXAMPLE),
        auto_flushing: int = DEFAULT_KAFKA_BATCH_FLUSH,
        use_tx: bool = DEFAULT_KAFKA_USE_TX,
        kafka_key: str = DEFAULT_KAFKA_DATA_KEY):
    """
    Универсальный маршрут для вставки данных в витрину
    """
    result = await InsertBodyJson(
        client,
        showcase,
        body,
        auto_flushing,
        use_tx,
        kafka_key
    ).insert()
    return result
