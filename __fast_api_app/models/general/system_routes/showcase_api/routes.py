from fastapi import APIRouter, Body, Depends
from fastapi_pagination import Params, paginate
from MODS.standart_namespace.routes import standardize_response
from .tools.select import showcase_select_base, showcase_select_union, EXAMPLE_SELECT_BASE, EXAMPLE_SELECT_UNION


router = APIRouter(
    prefix="/showcase",
    tags=["Showcases"],
    responses={404: {"description": "Not found"}},
)


@router.post("/select-base/{client_key}/{showcase_name}/")
@standardize_response
async def select_base_route(client_key: str, showcase_name: str, body=Body(..., example=EXAMPLE_SELECT_BASE)):
    """
    Универсальный маршрут для отправки select запроса к витрине
    """
    result = await showcase_select_base(client_key, showcase_name, body)
    return result


@router.post("/select-union/{client_key}/{showcase_name}/")
@standardize_response
async def select_union_route(client_key: str, body=Body(..., example=EXAMPLE_SELECT_UNION)):
    """
    Универсальный маршрут для отправки объединённых select запросов к витрине
    """
    result = await showcase_select_union(client_key, body)
    return result
