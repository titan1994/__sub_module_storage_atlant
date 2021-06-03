from MODS.storage_atlant_driver.pack_core.main import get_orm_class
from .get_model import ORMProcessingError
from tortoise import Tortoise
from MODS.rest_core.pack_core.aerich_proc import config as cfg_tortoise
from MODS.rest_core.pack_core.system_models.system_models import tortoise_state
from socket import gethostname
from os import getpid

async def delete_some(client_key, dict_name, **kwargs):
    """
    Получить список моделей, одну модель с фильтрацией.
    Пока что есть только получение списка без фильтра
    """
    obj_state = await tortoise_state.get(server=gethostname(), pid=getpid())
    if not obj_state.state:
        await Tortoise.init(config=cfg_tortoise.get_tortoise_config())
        obj_state.state=True
        await obj_state.save()
    class_model = get_orm_class(client_key=client_key, dict_name=dict_name)
    if not class_model:
        raise ORMProcessingError('Model not found!')

    if 'filter' in kwargs and kwargs['filter']:  # Фильтрация
        model_queryset = class_model.filter(**kwargs['filter'])
    else:
        model_queryset = class_model.all()

    res = await model_queryset.delete()

    return res