"""
Обработчик данных паспорта фермера
"""

import ijson
from tortoise.query_utils import Q
from starlette.datastructures import UploadFile
from pydantic import BaseModel, validator
from tortoise.contrib.pydantic import pydantic_model_creator

from MODS.DRIVERS.data_base.async_click_house import ycl
from MODS.DRIVERS.kafka_proc.driver import KafkaProducerConfluent

from MODS.storage_atlant_driver.pack_core.main import \
    get_orm_class, \
    gen_dict_table_name, \
    ycl_get_connection_settings

from GENERAL_CONFIG import GeneralConfig

CONST_DICT_NAME_ORGANIZATIONS = 'organizations'
CONST_KAFKA_DATA_KEY = 'ClickHouseMeansOfPassport'
CONST_USE_TX_CL_DATA_INPUT = False
CONST_BATCH_SIZE_DICT = 100


class MeansOfPassportProcessingError(Exception):
    pass


class PydClickHouseMeansOfPassport(BaseModel):
    subject: str = None
    period: str = None
    source_system: str = None
    source_form: str = None
    type: str = None
    economic_indicator: str = None
    code_score_ispkgp: str = None
    code_score_iscsapk: str = None
    data_generate: str = None
    value: float = None

    @validator(
        'subject', 'period', 'source_system', 'source_form', 'type',
        'economic_indicator', 'code_score_ispkgp', 'code_score_iscsapk', allow_reuse=True
    )
    def validate_subject(cls, v):
        if v == 'None':
            raise ValueError('If value is None must not to be.')
        return v.title()


async def client_post_processing_data(client_key, showcase, showcase_name, json_in, **kwargs):
    """
    Для каждого клиента свой обработчик данных на вставку
    """


    ClassORM = get_orm_class(client_key=client_key, dict_name=CONST_DICT_NAME_ORGANIZATIONS)
    ClassPYD = pydantic_model_creator(ClassORM)
    # primary_key = [key for key in ClassPYD.Config.fields.keys() if key in ClassORM._meta.pk_attr]

    kafka_topic_name = showcase.get('kafka_topic_name', None)
    if not kafka_topic_name:
        raise MeansOfPassportProcessingError('kafka is not settings!')

    summary_report = {
        'success_dict': 0,
        'success_data': 0,
        'error_in_dict': 0,
        'error_in_data': 0,
        'error_inn': 0
    }

    object_organizations = []
    FilterList = []

    if isinstance(json_in, UploadFile):
        # Ленивая обработка большого джсон файла

        json_async = ijson.items(json_in, 'item')
        async for data_obj in json_async:
            await process_one_obj(
                ClassORM=ClassORM,
                ClassPYD = ClassPYD,
                data_obj=data_obj,
                object_organizations=object_organizations,
                FilterList = FilterList,
                kafka_topic_name = kafka_topic_name,
                summary_report = summary_report
            )
    else:
        # Скозная/Как есть обработка джсона
        for data_obj in json_in:
            await process_one_obj(
                ClassORM = ClassORM,
                ClassPYD=ClassPYD,
                data_obj=data_obj,
                object_organizations=object_organizations,
                FilterList=FilterList,
                kafka_topic_name=kafka_topic_name,
                summary_report=summary_report
            )

    if len(object_organizations) > 0:
        await insert_data_to_base(
            ClassORM=ClassORM,
            ClassPYD=ClassPYD,
            object_organizations=object_organizations,
            FilterList = FilterList,
            summary_report=summary_report
        )

    # После вставки данных в словарь не забываем делать апдейт в кликхаусе.
    dict_update = [gen_dict_table_name(client_key=client_key, name_dict=CONST_DICT_NAME_ORGANIZATIONS)]
    conn = ycl_get_connection_settings(GeneralConfig.CLICKHOUSE_SHOWCASE_URL)
    try:
        await ycl.system_reload_dictionaries(conn=conn, names=dict_update)
    except Exception:
        pass

    return summary_report


async def process_one_obj(
        ClassORM,
        ClassPYD,
        data_obj,
        object_organizations,
        FilterList,
        kafka_topic_name,
        summary_report
):
    """
    Парсер одного объекта джсона
    """

    organization_inn = data_obj.get('organization', None)
    if not organization_inn:
        summary_report['error_inn'] = summary_report['error_inn'] + 1
        return

    # Понять есть ли словарь на редактирование
    property = data_obj.get('property', None)
    if property:
        # Создать словарь

        try:
            attr_create = {
                'INN': organization_inn,

                'subject': property.get('subject', ''),
                'OKTMO': property.get('OKTMO', ''),
                'contacts': property.get('contacts', ''),

                'KFH_registration_data': property.get('KFH', {}).get('registration_data', ''),
                'KFH_registration_address': property.get('KFH', {}).get('registration_address', ''),
                'KFH_full_name': property.get('KFH', {}).get('full_name', ''),
                'KFH_general_old': property.get('KFH', {}).get('general_old', ''),

                'grant_name': property.get('grant', {}).get('name', ''),
                'grant_type': property.get('grant', {}).get('type', ''),
                'grant_year': property.get('grant', {}).get('year', ''),
                'grant_size': property.get('grant', {}).get('size', 0),
                'grant_amount_own_funds': property.get('grant', {}).get('amount_own_funds', 0),
                'grant_amount_borrowed_funds': property.get('grant', {}).get('amount_borrowed_funds', 0),
                'grant_OKWED_KFH': property.get('grant', {}).get('OKWED_KFH', ''),
                'grant_OKWED_type': property.get('grant', {}).get('OKWED_type', ''),
                'grant_project_cost': property.get('grant', {}).get('project_cost', 0),
            }

            if not attr_create.get('KFH_registration_data', True):
                attr_create['KFH_registration_data'] = '0001-01-01T00:00:00'

            obj_pyd = ClassPYD(**attr_create)
            obj_orm = ClassORM(**obj_pyd.dict())

            object_organizations.append(obj_orm)
            FilterList.append(Q(INN=organization_inn, join_type='OR'))

        except Exception as exp:
            summary_report['error_in_dict'] = summary_report['error_in_dict'] + 1
            return

        if len(object_organizations) >= CONST_BATCH_SIZE_DICT:
            await insert_data_to_base(
                ClassORM=ClassORM,
                ClassPYD=ClassPYD,
                object_organizations=object_organizations,
                FilterList = FilterList,
                summary_report=summary_report
            )

            object_organizations.clear()
            FilterList.clear()

    # Вставить данные в кликхаус через кафку
    data_showcase = data_obj.get('data', None)
    if data_showcase:
        with KafkaProducerConfluent(
                use_tx=CONST_USE_TX_CL_DATA_INPUT,
                one_topic_name=kafka_topic_name,
                auto_flush_size=10000
        ) as kp:
            for sh_obj in data_showcase:
                if not sh_obj.get('data_generate', True):
                    sh_obj['data_generate'] = '0001-01-01T00:00:00'

                try:
                    obj_pyd = PydClickHouseMeansOfPassport(**sh_obj)
                    data_create = obj_pyd.dict()
                    data_create['organization'] = organization_inn

                    kp.put_data(
                        key=CONST_KAFKA_DATA_KEY,
                        value=data_create
                    )
                    summary_report['success_data'] = summary_report['success_data'] + 1

                except Exception as exp:
                    summary_report['error_in_data'] = summary_report['error_in_data'] + 1


async def insert_data_to_base(ClassORM, ClassPYD, FilterList, object_organizations, summary_report):
    """
    Пакетная вставка данных
    """

    try:
        found_org = await ClassORM.filter(Q(*FilterList, join_type='OR'))
        orgs_for_create = list(set(object_organizations) - set(found_org))
        if orgs_for_create:
            await ClassORM.bulk_create(objects=orgs_for_create, batch_size=CONST_BATCH_SIZE_DICT)

        if found_org:
            for org in found_org:
                new_data = object_organizations[object_organizations.index(org)]
                model_new = await ClassPYD.from_tortoise_orm(new_data)
                model_old = await ClassPYD.from_tortoise_orm(org)

                if model_new != model_old:
                    org.update_from_dict(data=model_new.dict())
                    await org.save()

        summary_report['success_dict'] = summary_report['success_dict'] + len(object_organizations)
    except Exception as exp:
        summary_report['error_in_dict'] = summary_report['error_in_dict'] + len(object_organizations)
