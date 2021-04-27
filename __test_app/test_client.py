from MODS.rest_core.pack_core.RUN.PRE_LAUNCH import APP_INIT
from MODS.MAIN_STRORAGE_BI.pack_core.HEART.client_api import test_processing_post_create, test_processing_delete
from MODS.MAIN_STRORAGE_BI.pack_core.psql_jsonb.connector import \
    get_client

import asyncio
from json import dump as jsd


async def test_get_client(client_key):
    result = await get_client(client_key=client_key)
    with open('z_get_jsonb_client_metadata.json', 'w', encoding='utf-8') as fb:
        jsd(result, fb, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    ioloop = asyncio.get_event_loop()
    ioloop.run_until_complete(test_processing_post_create())
    # ioloop.run_until_complete(test_processing_delete())