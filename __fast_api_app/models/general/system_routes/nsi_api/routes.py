"""
Универсальное API для работы с моделями
"""

from fastapi import APIRouter, Body, Depends
from fastapi_pagination import Params, paginate

from MODS.standart_namespace.routes import standardize_response

from .tools.create_model import create_some
from .tools.get_model import get_some
from .tools.delete_model import delete_some

router = APIRouter(
    prefix="/orm",
    tags=["ORM-Dictionaries"],
    responses={404: {"description": "Not found"}},
)

"""
Примеры
"""

EXAMPLE_POST_DICT_DATA = {
    "INN": "6829004230",
    "full_name": "Иванов Иван Иванович",
}

EXAMPLE_FILTER_ORDER_BODY = {
    "filter": {
        "federal_district": "Сибирский ФО",
        "code": "49",
    },
    "order_by": [
        "federal_district",
        "-OKTMO",
    ],
}

EXAMPLE_DELETE_FILTER_BODY = {
    "filter": {
        "federal_district": "Сибирский ФО",
        "code": "49",
    },
}

"""
Получение данных
"""


@router.get("/{client_key}/{dict_name}")
@standardize_response
async def orm_get_model_list(client_key: str, dict_name: str):
    """
    Универсальное получение списка
    """
    res = await get_some(
        client_key=client_key,
        dict_name=dict_name,
    )

    return res


@router.post("{client_key}/{dict_name}/filter")
@standardize_response
async def orm_get_model_list_filter(
        client_key: str,
        dict_name: str,
        body=Body(..., example=EXAMPLE_FILTER_ORDER_BODY)
):
    """
    Универсальное получение фильтрованного списка без пагинации
    """
    res = await get_some(
        client_key=client_key,
        dict_name=dict_name,
        filter=body.get('filter', None),
        order_by=body.get('order_by', None)
    )
    return res


@router.get("{client_key}/{dict_name}/{pk}")
@standardize_response
async def orm_get_model_by_pk(client_key: str, dict_name: str, pk: str):
    """
    Получение объекта по уникальному идентификатору
    """
    res = await get_some(
        client_key=client_key,
        dict_name=dict_name,
        filter={"pk": pk}
    )
    return res[0]


@router.get("/page/{client_key}/{dict_name}")
@standardize_response
async def orm_get_model_list_page(
        client_key: str,
        dict_name: str,
        params: Params = Depends()
):
    """
    Универсальное получение списка с пагинацией
    """

    res = await get_some(
        client_key=client_key,
        dict_name=dict_name,
    )
    page = paginate(res, params).json()
    return page


@router.post("/page/{client_key}/{dict_name}/filter")
@standardize_response
async def orm_get_model_list_filter_page(
        client_key: str,
        dict_name: str,
        params: Params = Depends(),
        body=Body(..., example=EXAMPLE_FILTER_ORDER_BODY)
):
    """
    Универсальное получение фильтрованного списка с пагинацией
    """
    res = await get_some(
        client_key=client_key,
        dict_name=dict_name,
        filter=body.get('filter', None),
        order_by=body.get('order_by', None)
    )
    page = paginate(res, params).json()
    return page


"""
Добавление данных
"""


@router.post("/{client_key}/{dict_name}")
@standardize_response
async def orm_post_model_list(
        client_key: str,
        dict_name: str,
        body=Body(..., example=EXAMPLE_POST_DICT_DATA)
):
    """
    Универсальная вставка модели
    """

    res = await create_some(
        client_key=client_key,
        dict_name=dict_name,
        body=body
    )

    return res


"""
Удаление данных
"""


@router.delete("{client_key}/{dict_name}/filter")
@standardize_response
async def orm_delete_model_list_filter(
        client_key: str,
        dict_name: str,
        body=Body(..., example=EXAMPLE_DELETE_FILTER_BODY)
):
    """
    Универсальное удаление фильтрованного списка
    """

    res = await delete_some(
        client_key=client_key,
        dict_name=dict_name,
        filter=body.get('filter', None),
    )
    return res


@router.delete("{client_key}/{dict_name}/{pk}")
@standardize_response
async def orm_delete_model_list_by_pk(client_key: str, dict_name: str, pk: str):
    """
    Удаление объекта по уникальному идентификатору
    """
    res = await delete_some(
        client_key=client_key,
        dict_name=dict_name,
        filter={"pk": pk}
    )
    return res
