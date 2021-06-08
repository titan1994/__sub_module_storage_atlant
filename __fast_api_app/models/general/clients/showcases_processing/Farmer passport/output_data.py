from MODS.DRIVERS.data_base.async_click_house import ycl

from MODS.storage_atlant_driver.pack_core.main import \
    ycl_get_connection_settings

from GENERAL_CONFIG import GeneralConfig


class ShowcaseFarmerPassportProcessingError(Exception):
    pass


"""
Обобщенный обработчик витрин
"""


async def client_get_data(client_key, showcase_name, table_name, json_in, **kwargs):
    """
    Получение данных витрин для клиента

    if showcase_name == ...
        skd_settings =...
    elif showcase_name == ...
        skd_settings =...
    """

    result = await means_of_passport_processor(
        client_key=client_key,
        showcase_name=showcase_name,
        table_name=table_name,
        json_in=json_in,
        kwargs=kwargs
    )

    # Когда витрин станет больше:
    # if showcase_name == 'means of passport':
    #     result = await means_of_passport_processor(
    #         client_key=client_key,
    #         showcase_name=showcase_name,
    #         table_name=table_name,
    #         json_in=json_in,
    #         kwargs=kwargs
    #     )
    # else:
    #     raise ShowcaseFarmerPassportProcessingError(f'invalid showcase name {showcase_name}')

    return result


"""
Значения витрины паспорта фермера
"""


async def means_of_passport_processor(client_key, showcase_name, table_name, json_in, **kwargs):
    """
    Значения паспорта фермера
    """

    try:
        organization = json_in['organization']
        subject = json_in['subject']

    except Exception:
        raise ShowcaseFarmerPassportProcessingError(
            'please include "organization" and "subject" fields in body package!')

    conn = ycl_get_connection_settings(GeneralConfig.CLICKHOUSE_SHOWCASE_URL)

    skd_settings = {
        'table_name': table_name,
        'db_name': json_in.get('db_name', None),
        'dimensions': [
            'organization',
            'subject',
            'period',
            'type',
            'economic_indicator',
            'farmerpassport_economic_indicators_npp',
            'farmerpassport_economic_indicators_parent',
            'source_system',
            'source_form',
            'farmerpassport_source_forms_property'
        ],
        'two_levels': ['farmerpassport_economic_indicators_parent', 'farmerpassport_source_forms_property'],
        'mesures': [
            {
                'name': 'value',
                'func': 'SUM'
            },
            {
                'name': 'data_generate',
                'func': 'max'
            }
        ],
        'filters': [
            {
                'name': 'organization',
                'value': organization,
            },
            {
                'name': 'subject',
                'value': subject,
            },
        ]
    }

    result = await ycl.select_skd_two_groups(
        conn=conn,
        data_select=skd_settings
    )

    report = []
    for row in result:
        if row['source_system'] == None:
            report.append(mop_parent_processing(row))
        else:
            report[-1]["group_data"].append(mop_group_data_processing(row))

    return report


def mop_parent_processing(row):
    """
    Верхний уровень данных
    """

    return {
        "organization": row['organization'],
        "subject": row["subject"],
        "period": row["period"],
        "type": row["type"],
        "economic_indicator": row["economic_indicator"],
        "economic_indicator_number": row["farmerpassport_economic_indicators_npp"],
        "economic_indicator_parent": row["farmerpassport_economic_indicators_parent"],
        "data_generate": row["data_generate"].isoformat(),
        "group_data": []
    }


def mop_group_data_processing(row):
    """
    Вложенные данные
    """

    return {
        "source_system": row['source_system'],
        "source_form": row['source_form'],
        "source_form_property": row['farmerpassport_source_forms_property'],
        "value": row['value'],
    }
