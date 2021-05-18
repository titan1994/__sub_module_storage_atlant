"""
Получение моделей ОРМ
"""

from fastapi.encoders import jsonable_encoder
from tortoise.contrib.pydantic import pydantic_model_creator

from MODS.storage_atlant_driver.pack_core.main import get_orm_class


class ORMProcessingError(Exception):
    pass


async def get_some(client_key, dict_name, **kwargs):
    """
    Получить список моделей, одну модель с фильтрацией.
    Пока что есть только получение списка без фильтра
    """

    class_model = get_orm_class(client_key=client_key, dict_name=dict_name)
    if not class_model:
        raise ORMProcessingError('Model not found!')

    pyd_model = pydantic_model_creator(class_model)
    if 'filter' in kwargs and kwargs['filter']: # Фильтрация
        model_queryset = class_model.filter(**kwargs['filter'])
    else:
        model_queryset = class_model.all()

    if 'order_by' in kwargs and kwargs['order_by']:  # Сортировка
        model_queryset = model_queryset.order_by(*kwargs['order_by'])

    model_list = await pyd_model.from_queryset(model_queryset)
    if not model_list:
        raise ORMProcessingError('Model`s items not found')

    res = jsonable_encoder(model_list)
    return res
