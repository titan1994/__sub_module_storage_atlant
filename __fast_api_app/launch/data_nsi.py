import asyncio
from pathlib import Path
from shutil import move, rmtree
from datetime import datetime
from json import load as jsl, dump as jsd
from pandas import read_excel

from tortoise.contrib.pydantic import pydantic_model_creator

from MODS.scripts.python.easy_scripts import PROJECT_GENERAL_FOLDER
from MODS.scripts.python.reg_ex import comb_file_name
from MODS.scripts.python.easy_scripts import get_include_object_from_catalog

from MODS.DRIVERS.pyxl.pandas_pyxl import PandasPyXlRW
from MODS.DRIVERS.data_base.async_click_house import ycl

from MODS.storage_atlant_driver.pack_core.main import \
    get_orm_class, \
    ycl_get_connection_settings, \
    gen_dict_table_name

from MODS.storage_atlant_driver.pack_core.HEART.client_api import \
    smart_create_client

from GENERAL_CONFIG import GeneralConfig

DEFAULT_PATH_TO_DATA = PROJECT_GENERAL_FOLDER / 'data_launch_system'


def first_run():
    """
    Функция будет выполнена после инициализации миграторов
    :return:
    """

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_create())


async def run_create():
    """
    Асинхронный обработчик создания первоначальных данных.
    Сначала создаёт клиента, затем отправляет данные словарей из xlsx в постгрес
    :return:
    """
    print('PROJECT DATA INIT RUN')

    # Запускаем тортоис
    from MODS.rest_core.pack_core.aerich_proc.config import TORTOISE_ORM
    from tortoise import Tortoise
    await Tortoise.init(config=TORTOISE_ORM)

    # Выполняем процедуру генерации клиентов из файловой системы
    await generate_default_client()

    # Выполняем процедуру генерации данных для словарей из xlsx
    await generate_data_for_dictionary()

    # Останавливаем тортоис
    await Tortoise.close_connections()
    print('PROJECT DATA INIT OK')


async def generate_default_client():
    """
    Атвогенератор клиентов из файловой системы
    """

    path_json_from = DEFAULT_PATH_TO_DATA / 'first_launch' / 'init_file_a_loads'
    path_json_to = DEFAULT_PATH_TO_DATA / 'first_launch' / 'init_file_z_ok'

    all_json_file = path_json_from.rglob(f'*.json')
    for file_settings in all_json_file:
        print(f'PROCESS JSON DATA CLIENT FROM FILE {file_settings.name}')
        try:
            with open(file_settings, 'r', encoding='utf-8') as file_read:
                json_data = jsl(file_read)

            name_file = set_time_to_file_name(file_settings.stem)
            res = await smart_create_client(json_data=json_data)

            with open(path_json_to / f'result_{name_file}{file_settings.suffix}', 'w', encoding='utf-8') as file_write:
                jsd(res, file_write, indent=4, ensure_ascii=False)

            move(src=file_settings, dst=path_json_to / f'process_{name_file}{file_settings.suffix}')
        except Exception as exp:
            print(exp)


async def generate_data_for_dictionary():
    """
    Генератор данных словарей.
    Основная идея:
    папка = имя клиента
    имя файла = имя словаря

    Данные в колонках имют порядок такой же как и при создании.
    Вот для чего данные колонок создаются из массива в джсоне!
    """

    global_dict_client_catalog_scan = DEFAULT_PATH_TO_DATA / 'dict_load_xlsx' / 'a_loads'
    global_dict_client_catalog_complete = DEFAULT_PATH_TO_DATA / 'dict_load_xlsx' / 'z_complete'

    list_client = get_include_object_from_catalog(src=global_dict_client_catalog_scan)

    dict_update = []
    for client in list_client:
        folder_scan = global_dict_client_catalog_scan / client
        folder_move = global_dict_client_catalog_complete / set_time_to_file_name(file_name=client, comb_name=False)

        print(f'PROCESS XLSX DATA DICTIONARY FROM FOLDER {client}')

        all_xlsx_file = folder_scan.rglob(f'*.xlsx')
        for file_dict in all_xlsx_file:

            dict_name = file_dict.stem
            print(f'GENERATE DATA DICTIONARY {dict_name}')

            OrmClass = get_orm_class(client_key=client, dict_name=dict_name)
            if OrmClass is None:
                print(f'dictionary {dict_name} from client {client} not found!')
                continue

            PydClass = pydantic_model_creator(OrmClass)

            with PandasPyXlRW(file_dict) as pd_xl:
                data_frame = read_excel(pd_xl.pd_writer, converters={'Наименование': str, 'наименование': str})

            primary_key = [key for key in PydClass.Config.fields.keys() if key in OrmClass._meta.pk_attr]
            for data in data_frame.values:
                try:
                    create_attr = {key: value for key, value in zip(PydClass.Config.fields.keys(), data)}
                    obj_pyd = PydClass(**create_attr)
                    data_create = obj_pyd.dict()

                    data_find = {key: value for key, value in data_create.items() if key in primary_key}
                    this_obj = await OrmClass.filter(**data_find).first()

                    if this_obj:
                        this_obj.update_from_dict(data=data_create)
                        await this_obj.save()
                    else:
                        await OrmClass.create(**data_create)

                except Exception as exp:
                    print(exp)

            dict_update.append(gen_dict_table_name(client_key=client, name_dict=dict_name))

        move(src=folder_scan, dst=folder_move)

    # После вставки данных в словарь не забываем делать апдейт в кликхаусе.
    if dict_update:
        conn = ycl_get_connection_settings(GeneralConfig.CLICKHOUSE_SHOWCASE_URL)
        try:
            await ycl.system_reload_dictionaries(conn=conn, names=dict_update)
        except Exception as exp:
            pass


def set_time_to_file_name(file_name, comb_name=True):
    """
    Добавление к имени файла даты
    """

    current_time = comb_file_name(datetime.now().isoformat())
    if comb_name:
        clean_up_file_name = comb_file_name(file_name)
    else:
        clean_up_file_name = file_name

    return f'{clean_up_file_name}__D__{current_time}'
