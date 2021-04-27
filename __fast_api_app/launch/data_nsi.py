import asyncio


def first_run():
    """
    Функция будет выполнена после инициализации миграторов
    :return:
    """

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_create())


async def run_create():
    """
    Асинхронный обработчик создания первоначальных данных TORTOISE
    :return:
    """
    print('FAST API INIT')

    # from tortoise import Tortoise
    # await Tortoise.init(config=TORTOISE_ORM)
    #
    # pattern, status = await Pattern.get_or_create(name=GeneralConfig.system_pattern['name'])
    # if status:
    #     pattern_serialized = await PYD_Pattern.from_tortoise_orm(pattern)
    #     response = pattern_serialized.json()
    #
    #     print('First create pattern')
    #     print(response)
    #
    # await Tortoise.close_connections()
