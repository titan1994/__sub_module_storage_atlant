from MODS.storage_atlant_driver.pack_core.main import get_orm_class
from .get_model import ORMProcessingError


async def delete_some(client_key, dict_name, **kwargs):
    """
    Получить список моделей, одну модель с фильтрацией.
    Пока что есть только получение списка без фильтра
    """

    class_model = get_orm_class(client_key=client_key, dict_name=dict_name)
    if not class_model:
        raise ORMProcessingError('Model not found!')

    if 'filter' in kwargs and kwargs['filter']:  # Фильтрация
        model_queryset = class_model.filter(**kwargs['filter'])
    else:
        model_queryset = class_model.all()

    res = await model_queryset.delete()

    return res