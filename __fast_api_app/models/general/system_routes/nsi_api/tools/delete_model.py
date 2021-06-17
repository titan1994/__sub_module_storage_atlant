from MODS.storage_atlant_driver.pack_core.main import get_orm_class
from .get_model import ORMProcessingError
from GENERAL_CONFIG import GeneralConfig
from MODS.rest_core.pack_core.system_models.system_models import tortoise_state
from MODS.DRIVERS.data_base.async_click_house.ycl import system_reload_dictionaries
from MODS.storage_atlant_driver.pack_core.main import ycl_get_connection_settings


async def delete_some(client_key, dict_name, **kwargs):
    """
    Получить список моделей, одну модель с фильтрацией.
    Пока что есть только получение списка без фильтра
    """
    state = await tortoise_state.state_check()
    if not state:
        await tortoise_state.state_activate()
    class_model = get_orm_class(client_key=client_key, dict_name=dict_name)
    if not class_model:
        raise ORMProcessingError('Model not found!')
    table_names = [class_model.describe()['table']]
    if 'filter' in kwargs and kwargs['filter']:  # Фильтрация
        model_queryset = class_model.filter(**kwargs['filter'])
    else:
        model_queryset = class_model.all()

    res = await model_queryset.delete()

    conn = ycl_get_connection_settings(GeneralConfig.CLICKHOUSE_SHOWCASE_URL)
    try:
        await system_reload_dictionaries(conn=conn, names=table_names)
    except Exception:
        pass

    return res