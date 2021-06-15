import asyncio
from inspect import getfile as inspect_getfile
from pathlib import Path
import shutil

DEFAULT_PATH_PATCH = Path(__file__).parent / '__patch_filters.py'


def first_run():
    """
    Функция будет выполнена после инициализации миграторов
    :return:
    """

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_create())


async def run_create():
    """
    Патч библиотеки тортоиса для работы с jsonb
    :return:
    """

    try:
        from tortoise.filters import JsonbFounder
        print('JSONB PATCH ALREADY INSTALL')

    except Exception:

        from tortoise.filters import Like
        path_patch = inspect_getfile(Like)

        shutil.copyfile(src=DEFAULT_PATH_PATCH.absolute(), dst=Path(path_patch).absolute())

        print('JSONB PATCH SUCCESS INSTALL')
