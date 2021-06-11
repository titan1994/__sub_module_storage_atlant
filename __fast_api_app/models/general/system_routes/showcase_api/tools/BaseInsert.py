from abc import ABC, abstractmethod
import ijson
from json import loads as jsl
from pydantic import create_model, validator
from typing import Optional

from .settings import get_showcase_data
from .validators import uint_valid, uuid_valid, datetime_valid

from MODS.DRIVERS.kafka_proc.driver import KafkaProducerConfluent


class InsertShowcase(ABC):
    """
    Шаблоннный класс для вставки данных в витрину
    Имеет методы общие для каждого класса
    Имеет методы, которые обязательно нужно реализовать в наследниках
    """
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

    def __init__(self, client, showcase, data, auto_flush, use_tx, kafka_key):
        self.client = client
        self.showcase = showcase
        self.data = data
        self.auto_flush = auto_flush
        self.use_tx = use_tx
        self.kafka_key = kafka_key
        self.summary_report = {
            'count_success_input': 0,
            'count_error_input': 0,
        }

    async def insert(self) -> dict:
        """
        Шаблонный метод определяет скелет алгоритма вставки.
        """
        await self.get_metadata()
        self.columns_to_pd_attr()
        self.validators_create()
        self.create_pd_model()
        self.data_transform()
        with self.create_connection_kafka() as self.KP:
            await self.validate_send_kafka()
        return self.summary_report

    # Эти операции уже имеют реализации.

    async def get_metadata(self):
        """
        Получает данные о витрине из стороннего хранилища
        """
        metadata = await get_showcase_data(client_key=self.client, showcase_name=self.showcase)
        if self.kafka_key is None:
            self.kafka_key = metadata['ycl_table_showcase_data']
        self.required = metadata['target_table']['order_by']
        self.kafka_topic = metadata['kafka_topic_name']
        self.columns_clickhouse = metadata['target_table']['columns']

    def columns_to_pd_attr(self):
        """
        Преобразует типы данных кликхауса в питонячьи
        """
        new_columns = {}
        for name, value in self.columns_clickhouse.items():
            if value['type'] in self.types_mapping.keys():
                if name not in self.required:
                    new_columns[name] = (Optional[self.types_mapping[value['type']]], None)
                else:
                    new_columns[name] = (self.types_mapping[value['type']], ...)
        self.columns = new_columns

    def validators_create(self):
        """
        Тут в зависимости от поля вешаются на них валидационные функции
        """
        validators = {}
        for name, value in self.columns_clickhouse.items():
            if 'DateTime' in value['type']:
                validators[name + 'validator'] = validator(name, allow_reuse=True)(datetime_valid)
            if 'UUID' in value['type']:
                validators[name + 'validator'] = validator(name, allow_reuse=True)(uuid_valid)
            if 'UInt' in value['type']:
                validators[name + 'validator'] = validator(name, allow_reuse=True)(uint_valid)
        self.validators = validators

    def create_pd_model(self):
        """
        Создаём класс pydantic для валидации
        """
        self.PD_class = create_model('PD_{0}_{1}'.format(self.client, self.showcase), **self.columns,
                                     __validators__=self.validators)

    def create_connection_kafka(self):
        """
        Создание объекта соединения к кафке
        """
        return KafkaProducerConfluent(
            use_tx=self.use_tx,
            one_topic_name=self.kafka_topic,
            auto_flush_size=self.auto_flush)

    def send_to_kafka(self, data):
        """
        Отправление строки в кафку

        """
        try:
            data = self.validate_get_dict(data)
            self.KP.put_data(
                key=self.kafka_key,
                value=data
            )
            self.summary_report['count_success_input'] += 1
        except Exception as exp:
            self.summary_report['count_error_input'] += 1

    def validate_get_dict(self, row):
        """
        проверка данных pydantic
        """
        obj = self.PD_class(**row)
        data_create = obj.dict(exclude_none=True)
        return data_create

    # А эти операции должны быть реализованы в подклассах.
    @abstractmethod
    def data_transform(self):
        """
        Тут нужно трансформировать и предпроверять входные данные
        """
        pass

    @abstractmethod
    async def validate_send_kafka(self):
        """
        тут вызывать self.send_to_kafka(row) для каждой записи,
        которую надо положитьв кафку
        """
        pass


class InsertFileLarge(InsertShowcase):
    """
    Вставка данных из большого файла
    """

    def data_transform(self):
        self.data = ijson.items(self.data, 'item')

    async def validate_send_kafka(self):
        async for row in self.data:
            self.send_to_kafka(row)


class InsertFileSmall(InsertShowcase):
    """
    Вставка данных из маленького файла
    """

    def data_transform(self):
        self.data = jsl(self.data)

    async def validate_send_kafka(self):
        for row in self.data:
            self.send_to_kafka(row)


class InsertBodyJson(InsertShowcase):
    """
    Вставка данных из тела json
    """

    def data_transform(self):
        if isinstance(self.data, dict):
            self.data = [self.data]

    async def validate_send_kafka(self):
        for row in self.data:
            self.send_to_kafka(row)
