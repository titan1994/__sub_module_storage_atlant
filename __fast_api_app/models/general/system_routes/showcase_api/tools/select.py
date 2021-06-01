from GENERAL_CONFIG import GeneralConfig
from MODS.DRIVERS.data_base.async_click_house.ycl import select_base, select_union
from MODS.storage_atlant_driver.pack_core.main import ycl_get_connection_settings
from .settings import get_showcase_data

EXAMPLE_SELECT_BASE = {
    "fields": [
        {
            "name": "pk",
            "func": "count",
            "alias": "biba"
        }
    ],
    "distinct": True,
    "filters": [
        {
            'name': 'subject',
            'value': '01'
        }
    ],
    "pre_filters": [
        {
            'name': 'period',
            'value': '2020'
        }
    ],
    "group_by": ['period'],
    "group_by_with": 'CUBE',
    "order_by": ['period'],
    "having": [
        {
            'name': 'period',
            'value': '2020'
        }
    ]
}

EXAMPLE_SELECT_UNION = {
    "selects": [
        {
            "showcase":"Passport KFH",
            "fields": [
                {
                    "name": "INN",
                    "func": "count",
                    "alias": "alternative_name"
                }
            ],
            "union": "ALL"
        },
        {
            "showcase":"Passport KFH",
            "fields": [
                {
                    "name": "INN",
                    "func": "count",
                    "alias": "alternative_name"
                }
            ],
            "union": "ALL"
        }
    ]
}


async def showcase_select_base(client_key, showcase_name, data):
    meta_data = await get_showcase_data(client_key, showcase_name)
    data['table'] = meta_data['target_table']['table_name']
    conn = ycl_get_connection_settings(GeneralConfig.CLICKHOUSE_SHOWCASE_URL)
    res = await select_base(conn, data)
    return res


async def showcase_select_union(client_key, data):
    for select in data['selects']:
        meta_data = await get_showcase_data(client_key, select['showcase'])
        select['table'] = meta_data['target_table']['table_name']
    conn = ycl_get_connection_settings(GeneralConfig.CLICKHOUSE_SHOWCASE_URL)
    res = await select_union(conn, data)
    return res
