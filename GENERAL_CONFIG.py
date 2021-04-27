"""
Основная конфигурация проекта.
Сначала мы решаем какое ядро используем - потом наследуем его в GeneralConfig
"""

from MODS.scripts.python.easy_scripts import PROJECT_GENERAL_FOLDER as general_path
from multiprocessing import cpu_count

from abc import ABC, abstractmethod
from enum import Enum


class AppMode(Enum):
    """
    Режим развертки приложения продуктив/отладка
    """

    debug = 'debug'
    production = 'production'


class NoObjectMixin(ABC):
    """
    Защита от супер умных - экземпляры рождать нельзя
    """

    @abstractmethod
    def __no_object(self):
        pass


class FastApiConfig(NoObjectMixin):
    """
    Конфигурация фаст-апи
    """

    """
    AERICH + TORTOISE
    """

    # путь по регламенту тортоиса к конфигуратору тортоиса (В МОДУЛЕ РАСКОММЕНТИРОВАТЬ ПЕРВОЕ!)
    # DEFAULT_AERICH_CFG_PATH = 'MODS.rest_core.pack_core.aerich_proc.config.TORTOISE_ORM'
    DEFAULT_AERICH_CFG_PATH = 'pack_core.aerich_proc.config.TORTOISE_ORM'

    # Основная папка с моделями тортоиса
    DEFAULT_AERICH_MODEL_PACK_PATH = '__fast_api_app.models'

    # путь к папке с миграциями для тортоиса
    DEFAULT_AERICH_MIGR_PATH = general_path / '__migrations' / 'aerich'

    # путь к файлу хранения конфигурации .ini
    DEFAULT_AERICH_INI_FILE = general_path / 'aerich.ini'
    DEFAULT_AERICH_INI_PATH = general_path / '__migrations' / 'aerich' / 'aerich.ini'

    # папка в которую смотрит анализатор моделей и ищет их там
    DEFAULT_AERICH_MODEL_APP_PATH = \
        general_path / DEFAULT_AERICH_MODEL_PACK_PATH.replace('.', '/') / 'general'


"""
Наследованием выбираем ядро-фреймворк. 
Дописываем общие для всех фреймворков параметры конфигурации
"""


class GeneralConfig(FastApiConfig):
    """
    Общая конфа - она импортируется по проекту
    """
    PROJECT_NAME = 'Ядро фаст апи. Submodule'  # Open API спецификация чувствительна к имени - будьте осторожны
    DEFAULT_APP_MODE = AppMode.debug
    DEFAULT_PORT = 5111  # Порт

    DEFAULT_DB_URI = None
    ITS_DOCKER = None

    PROJECT_GENERAL_FOLDER = general_path
    DEFAULT_WORKER_COUNT = cpu_count() + 1
