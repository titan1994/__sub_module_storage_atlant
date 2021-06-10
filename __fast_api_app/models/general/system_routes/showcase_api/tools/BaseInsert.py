from abc import ABC, abstractmethod
from json import loads as jsl
from .settings import get_showcase_data
from pydantic import create_model, validator
from .validators import uint_valid, uuid_valid, datetime_valid
from typing import Optional
from MODS.DRIVERS.kafka_proc.driver import KafkaProducerConfluent


class InsertShowcase(ABC):
    """

    """
    summary_report = {
        'count_success_input': 0,
        'count_error_input': 0,
    }


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

    async def insert(self) -> dict:
        """
        Шаблонный метод определяет скелет алгоритма.
        """
        await self.get_metadata()
        self.columns_to_pd_attr()
        self.validators_create()
        self.columns_to_pd_attr()
        self.create_connection_kafka()
        await self.validate_send_kafka()
        return self.summary_report

    # Эти операции уже имеют реализации.

    async def get_metadata(self) -> None:
        metadata = await get_showcase_data(client_key=self.client, showcase_name=self.showcase)
        if self.kafka_key is None:
            self.kafka_key = metadata['ycl_table_showcase_data']
        self.required = metadata['target_table']['order_by']
        self.kafka_topic = metadata['kafka_topic_name']
        self.columns_clickhouse = metadata['target_table']['columns']


    def validators_create(self) -> dict:
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

    def columns_to_pd_attr(self) -> dict:
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

    def create_pd_model(self):
        self.PD_class = create_model('PD_{0}_{1}'.format(self.client, self.showcase), **self.columns,
                                     __validators__=self.validators)

    def create_connection_kafka(self):
        self.KP = KafkaProducerConfluent(
                use_tx=self.use_tx,
                one_topic_name=self.kafka_topic,
                auto_flush_size=self.auto_flush)


    def send_to_kafka(self, data):
        try:
            with self.KP as kp:
                kp.put_data(
                    key=self.kafka_key,
                    value=data
                )
            self.summary_report['count_success_input'] += 1
        except Exception as exp:
            self.summary_report['count_error_input'] += 1


    def validate_get_dict(self, row):
        obj = self.PD_class(**row)
        data_create = obj.dict(exclude_none=True)
        return data_create


    # А эти операции должны быть реализованы в подклассах.
    @abstractmethod
    async def validate_send_kafka(self) -> dict:
        pass


class InsertFileLarge(InsertShowcase):
    """
    Вставка данных из большого файла
    """
    async def validate_send_kafka(self) -> dict:
        async for row in self.data:
            self.send_to_kafka(row)
        return self.summary_report


class InsertFileSmall(InsertShowcase):
    """
    Вставка данных из маленького файла
    """
    async def validate_send_kafka(self) -> dict:
        self.data = jsl(self.data)
        for row in self.data:
            self.send_to_kafka(row)
        return self.summary_report

class InsertBodyJson(InsertShowcase):
    """
    Вставка данных из тела json
    """
    async def validate_send_kafka(self) -> dict:
        if isinstance(self.data, dict):
            self.data = [self.data]
        for row in self.data:
            self.send_to_kafka(row)
        return self.summary_report