import ijson

from json import loads as jsl
from pydantic import validator
from typing import Optional
from pydantic import create_model

from MODS.DRIVERS.kafka_proc.driver import KafkaProducerConfluent

from .settings import get_showcase_data
from .validators import datetime_valid, uuid_valid, uint_valid
from .input_formats import FormatTypes

types_mapping = {
    'String': str,
    'Int32': int,
    'Int16': int,
    'Int8': int,
    'Int4': int,
    'Int64': int,
    'UInt32': int,
    'UInt16': int,
    'UInt8': int,
    'UInt4': int,
    'UInt64': int,
    'Float32': float,
    'Float64': float,
    'Date': str,
    'DateTime': str,
    'UUID': str,
}

INSERT_EXAMPLE = {
    "INN": "112233",
    "Size": 1,
    "MaxPart": 1000
}


async def showcase_insert_universal(client, showcase, data, auto_flush, use_tx, kafka_key, input_format=None):
    """
    asunc_check - True если файл большой и data нужно читать асинхронно
    функция для вставки данных в витрину через кафку
    Вход - имя клиента, имя витрины, данные для вставки
    Шаг 1. Проверить есть ли такая витрина, получить имя топика кафки
    Шаг 2. Создать класс Pydantic и валидировать данные
    Шаг 3. Отправить данные в кафку
    return суммарный отчёт
    """

    """
    Первичный анализ данных
    """
    summary_report = {
        'count_success_input': 0,
        'count_error_input': 0,
    }
    metadata = await get_showcase_data(client, showcase)
    if kafka_key is None:
        kafka_key = metadata['ycl_table_showcase_data']
    columns = columns_to_pd_attr(metadata['target_table']['columns'], metadata['target_table']['order_by'])
    validators = validators_create(metadata['target_table']['columns'])
    PD_class = create_model('PD_{0}_{1}'.format(client, showcase), **columns, __validators__=validators)

    """
    Подготовка данных
    """

    if input_format in [FormatTypes.body_json, FormatTypes.file_small_json]:

        if input_format == FormatTypes.file_small_json:
            data = jsl(data)

        if isinstance(data, dict):
            # если это одна запись - надо сделать список из неё
            data = [data]

    elif input_format == FormatTypes.file_large_json:
        data = ijson.items(data, 'item')
    else:
        raise ValueError(f'Unsupported format types data {input_format}')

    """
    ОБработка данных
    """

    with KafkaProducerConfluent(
            use_tx=use_tx,
            one_topic_name=metadata['kafka_topic_name'],
            auto_flush_size=auto_flush
    ) as kp:

        if async_check:  # проверка на ассинхронность data - если файл большой - читаем лениво
            async for row in data:
                summary_report = process_one_object(PD_class, row, kp, kafka_key, summary_report)
        else:
            for row in data:
                summary_report = process_one_object(PD_class, row, kp, kafka_key, summary_report)

    return summary_report


def process_one_object(PD_class, row, kp, kafka_key, summary_report):
    """
    Валидация и отправка в кафку
    """
    try:
        obj = PD_class(**row)
        data_create = obj.dict(exclude_none=True)
        kp.put_data(
            key=kafka_key,
            value=data_create
        )
        summary_report['count_success_input'] = summary_report['count_success_input'] + 1

    except Exception as exp:
        summary_report['count_error_input'] = summary_report['count_error_input'] + 1

    return summary_report


def columns_to_pd_attr(columns: dict, required: list) -> dict:
    """
    Преобразует типы данных кликхауса в питонячьи
    """
    new_columns = {}
    for name, value in columns.items():
        if value['type'] in types_mapping.keys():
            if name not in required:
                new_columns[name] = (Optional[types_mapping[value['type']]], None)
            else:
                new_columns[name] = (types_mapping[value['type']], ...)
    return new_columns


def validators_create(columns: dict) -> dict:
    """
    Тут в зависимости от поля вешаются на них валидационные функции
    """
    validators = {}
    for name, value in columns.items():
        if 'DateTime' in value['type']:
            validators[name + 'validator'] = validator(name, allow_reuse=True)(datetime_valid)
        if 'UUID' in value['type']:
            validators[name + 'validator'] = validator(name, allow_reuse=True)(uuid_valid)
        if 'UInt' in value['type']:
            validators[name + 'validator'] = validator(name, allow_reuse=True)(uint_valid)
    return validators
