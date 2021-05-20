"""
Обработчик данных паспорта фермера
"""

from pydantic import BaseModel, validator
from tortoise.contrib.pydantic import pydantic_model_creator

from MODS.DRIVERS.data_base.async_click_house import ycl
from MODS.DRIVERS.kafka_proc.driver import KafkaProducerConfluent

from MODS.storage_atlant_driver.pack_core.main import \
    get_orm_class, \
    gen_dict_table_name, \
    ycl_get_connection_settings

from GENERAL_CONFIG import GeneralConfig


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
    value: float = None

    @validator(
        'subject', 'period', 'source_system', 'source_form', 'type',
        'economic_indicator', 'code_score_ispkgp', 'code_score_iscsapk', allow_reuse=True
    )
    def validate_subject(cls, v):
        if v == 'None':
            raise ValueError('If value is None must not to be.')
        return v.title()


async def process_input_data(client_key, showcase, showcase_name, json_in, **kwargs):
    """
    Для каждого клиента свой обработчик данных на вставку
    """

    CONST_DICT_NAME_ORGANIZATIONS = 'organizations'
    CONST_KAFKA_DATA_KEY = 'ClickHouseMeansOfPassport'
    CONST_USE_TX_CL_DATA_INPUT = False

    ClassORM = get_orm_class(client_key=client_key, dict_name=CONST_DICT_NAME_ORGANIZATIONS)
    ClassPYD = pydantic_model_creator(ClassORM)
    primary_key = [key for key in ClassPYD.Config.fields.keys() if key in ClassORM._meta.pk_attr]

    kafka_topic_name = showcase.get('kafka_topic_name', None)
    if not kafka_topic_name:
        raise MeansOfPassportProcessingError('kafka is not settings!')

    summary_report = {
        'input_object': len(json_in),
        'success': 0,
        'error_in_dict': 0,
        'error_in_data': 0,
        'error_inn': 0,
        'ycl_status': 'OK'
    }

    for data_obj in json_in:
        # Получить ИНН
        success_processing = True

        organization_inn = data_obj.get('organization', None)
        if not organization_inn:
            summary_report['error_inn'] = summary_report['error_inn'] + 1
            continue

        # Понять есть ли словарь на редактирование
        property = data_obj.get('property', None)
        if property:
            # Создать словарь

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

            try:
                obj_pyd = ClassPYD(**attr_create)
                data_create = obj_pyd.dict()

                data_find = {key: value for key, value in data_create.items() if key in primary_key}
                this_obj = await ClassORM.filter(**data_find).first()

                if this_obj:
                    this_obj.update_from_dict(data=data_create)
                    await this_obj.save()
                else:
                    await ClassORM.create(**data_create)

            except Exception as exp:
                summary_report['error_in_dict'] = summary_report['error_in_dict'] + 1
                success_processing = False

        # Вставить данные в кликхаус через кафку
        data_showcase = data_obj.get('data', None)
        if data_showcase:
            with KafkaProducerConfluent(
                    use_tx=CONST_USE_TX_CL_DATA_INPUT,
                    one_topic_name=kafka_topic_name
            ) as kp:
                for sh_obj in data_showcase:
                    try:
                        obj_pyd = PydClickHouseMeansOfPassport(**sh_obj)
                        data_create = obj_pyd.dict()
                        data_create['organization'] = organization_inn

                        kp.put_data(
                            key=CONST_KAFKA_DATA_KEY,
                            value=data_create
                        )
                    except Exception as exp:
                        summary_report['error_in_data'] = summary_report['error_in_data'] + 1
                        success_processing = False

        if success_processing:
            summary_report['success'] = summary_report['success'] + 1

    # После вставки данных в словарь не забываем делать апдейт в кликхаусе.
    dict_update = [gen_dict_table_name(client_key=client_key, name_dict=CONST_DICT_NAME_ORGANIZATIONS)]
    conn = ycl_get_connection_settings(GeneralConfig.CLICKHOUSE_SHOWCASE_URL)
    try:
        await ycl.system_reload_dictionaries(conn=conn, names=dict_update)
    except Exception as exp:
        summary_report['ycl_status'] = str(exp)

    return summary_report
