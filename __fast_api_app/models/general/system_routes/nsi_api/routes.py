"""
Универсальное API для работы с моделями
"""

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi_pagination import Params, paginate
from typing import Optional

from MODS.standart_namespace.routes import standardize_response
from .tools.create_model import create_some
from .tools.get_model import get_some

router = APIRouter(
    prefix="/orm",
    tags=["ORM-Dictionaries"],
    responses={404: {"description": "Not found"}},
)


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


@router.post("/{client_key}/{dict_name}")
@standardize_response
async def orm_post_model_list(client_key: str, dict_name: str, body=Body(...)):
    """
    Универсальная вставка модели
    """

    res = await create_some(
        client_key=client_key,
        dict_name=dict_name,
        body=body
    )

    return res


@router.get("/page/{client_key}/{dict_name}")
@standardize_response
async def orm_get_model_list_page(client_key: str, dict_name: str, params: Params = Depends()):
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
async def orm_get_model_list_filter_page(client_key: str, dict_name: str, params: Params = Depends(),
                                         body=Body(...)):
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


@router.get("/page/{client_key}/{dict_name}/{pk}")
@standardize_response
async def orm_get_model_by_pk(client_key: str, dict_name: str, pk: Optional[str], params: Params = Depends()):
    """
    Получение объекта по уникальному идентификатору
    """
    res = await get_some(
        client_key=client_key,
        dict_name=dict_name,
        filter={"pk": pk}
    )
    return res[0]
