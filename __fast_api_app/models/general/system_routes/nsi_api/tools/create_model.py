"""
Создание моделей ОРМ
"""

from json import loads as jsl
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import ValidationError
from MODS.rest_core.pack_core.system_models.system_models import tortoise_state
from MODS.storage_atlant_driver.pack_core.main import get_orm_class
from MODS.DRIVERS.data_base.async_click_house.ycl import system_reload_dictionaries
from GENERAL_CONFIG import GeneralConfig
from MODS.storage_atlant_driver.pack_core.main import ycl_get_connection_settings


class ORMCreateError(Exception):
    pass


class PydanticCreateError(Exception):
    pass


async def create_some(client_key, dict_name, body):
    """
    Универсальная вставка модели
    """
    state = await tortoise_state.state_check()
    if not state:
        await tortoise_state.state_activate()
    class_model = get_orm_class(client_key=client_key, dict_name=dict_name)
    if not class_model:
        raise ORMCreateError('Model not found!')

    pyd_model = pydantic_model_creator(class_model)

    table_names = [class_model.describe()['table']]

    global_response = []
    if isinstance(body, dict):
        # Вставка одного объекта

        res = await model_create(
            ClassOrm=class_model,
            ClassPyd=pyd_model,
            data_model=body,
            soft_insert=False
        )
        global_response.append(res)
    else:
        # Вставка нескольких объектов

        for data_mod in body:
            res = await model_create(
                ClassOrm=class_model,
                ClassPyd=pyd_model,
                data_model=data_mod,
                soft_insert=True
            )
            global_response.append(res)

    conn = ycl_get_connection_settings(GeneralConfig.CLICKHOUSE_SHOWCASE_URL)
    try:
        await system_reload_dictionaries(conn=conn, names=table_names)
    except Exception:
        pass

    return global_response


async def model_create(ClassOrm, ClassPyd, data_model, soft_insert):
    """
    Универсальное создание моделей с использованием пидантика
    """

    general_response = {
        'status': False,
        'data': None
    }

    # Шаг 1 валидация
    try:
        obj_pyd = ClassPyd(**data_model)
    except ValidationError as exp:
        if soft_insert:
            general_response['data'] = jsl(exp.json())
            return general_response
        else:
            raise PydanticCreateError(exp.json())

    # Шаг 2 Создание
    try:
        orm_obj = await ClassOrm.create(**obj_pyd.dict())
    except Exception as exp:
        if soft_insert:
            general_response['data'] = str(exp)
            return general_response
        else:
            raise ORMCreateError(str(exp))

    # Шаг 3 Ответ
    back_proc = await ClassPyd.from_tortoise_orm(orm_obj)
    general_response['data'] = back_proc.dict()
    general_response['status'] = True

    return general_response
