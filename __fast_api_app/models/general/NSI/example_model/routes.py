from fastapi import APIRouter
from MODS.standart_namespace.routes import standardize_response

from .models import ExampleModel
from .pydantic import PYD_ExampleModel

router = APIRouter(
    prefix="/example_model",
    tags=["example model"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{id}")
@standardize_response
async def get(id: str):
    pattern = await ExampleModel.get(id=id)
    pattern_serialized = await PYD_ExampleModel.from_tortoise_orm(pattern)
    return pattern_serialized.json()


