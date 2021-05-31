from GENERAL_CONFIG import GeneralConfig
from MODS.DRIVERS.data_base.async_click_house.ycl import select_base, select_union
from MODS.storage_atlant_driver.pack_core.main import ycl_get_connection_settings

EXAMPLE_SELECT_BASE = {
    "table": "__cl_smpb_showcase_data_farmerpassport_meansofpassport",
    "fields": [
        "count(subject)",
        "period"
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
            "table": "__cl_smpb_nsi_farmerpassport_source_forms",
            "fields": [
                "name",
                "code"
            ],
            "union": "ALL"
        },
        {
            "table": "__cl_smpb_nsi_farmerpassport_source_forms",
            "fields": [
                "name",
                "code"
            ],
            "union": "ALL"
        }
    ]
}


async def showcase_select_base(data):
    conn = ycl_get_connection_settings(GeneralConfig.CLICKHOUSE_SHOWCASE_URL)
    res = await select_base(conn, data)
    return res


async def showcase_select_union(data):
    conn = ycl_get_connection_settings(GeneralConfig.CLICKHOUSE_SHOWCASE_URL)
    res = await select_union(conn, data)
    return res
