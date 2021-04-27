from fastapi import APIRouter
from MODS.standart_namespace.routes import standardize_response

router = APIRouter(
    prefix="/test_app",
    tags=["test app"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
@standardize_response
async def get():
    return {'state': 'server ok'}
