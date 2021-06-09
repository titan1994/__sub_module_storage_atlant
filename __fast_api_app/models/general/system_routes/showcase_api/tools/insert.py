import datetime

from .settings import get_showcase_data
from pydantic import create_model
from MODS.DRIVERS.kafka_proc.driver import KafkaProducerConfluent
from .validators import datetime_valid, uuid_valid, uint_valid
from GENERAL_CONFIG import GeneralConfig
from pydantic import validator, BaseModel
from typing import Optional

CONST_KAFKA_DATA_KEY = 'FROM_API'
CONST_USE_TX_CL_DATA_INPUT = False


async def showcase_insert_universal(client, showcase, data):
    """
    функция для вставки данных в витрину через кафку
    Вход - имя клиента, имя витрины, данные для вставки
    Шаг 1. Проверить есть ли такая витрина, получить имя топика кафки
    Шаг 2. Создать класс Pydantic и валидировать данные
    Шаг 3. Отправить данные в кафку
    """
    summary_report = {
        'success_showcase': 0,
        'error_in_showcase': 0,
    }

    metadata = await get_showcase_data(client, showcase)
    columns = columns_to_pd_attr(metadata['target_table']['columns'], metadata['target_table']['order_by'])
    validators = validators_create(metadata['target_table']['columns'])
    PD_class = create_model('PD_{0}_{1}'.format(client, showcase), **columns, __validators__=validators)
    if not isinstance([], list):
        data = [data]
    with KafkaProducerConfluent(
            use_tx=CONST_USE_TX_CL_DATA_INPUT,
            one_topic_name=metadata['kafka_topic_name'],
            auto_flush_size=1000
    ) as kp:
        for row in data:
            try:
                obj = PD_class(**row)
                data_create = obj.dict(exclude_none=True)
                kp.put_data(
                    key=CONST_KAFKA_DATA_KEY,
                    value=data_create
                )
                summary_report['success_showcase'] = summary_report['success_showcase'] + 1
            except Exception as exp:
                summary_report['error_in_showcase'] = summary_report['error_in_showcase'] + 1
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
    "INN":"112233",
    "Size":1,
    "MaxPart":1000
}