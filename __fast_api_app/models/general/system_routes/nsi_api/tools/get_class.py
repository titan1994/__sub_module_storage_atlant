"""
Получение классов ОРМ
"""

from MODS.rest_core.pack_core.RUN.__tools.tortoise import models_inspector

from importlib import import_module
from inspect import getmembers, isclass


def get_orm_class(client_key, dict_name):
    """
    Получить класс модели ОРМ по ключу клиента и имени словаря
    Имена совпадают один к одному в конфигурации метаданных
    """
    for mod_name in models_inspector():
        mod = import_module(mod_name)
        class_models = (
            m[1] for m in getmembers(mod, isclass)
            if m[1].__module__ == mod.__name__
               and client_key == getattr(m[1], '__original_client_name__', '')
               and dict_name == getattr(m[1], '__original_dict_name__', '')
        )

        for class_obj in class_models:
            return class_obj

    return None

