from MODS.rest_core.pack_core.RUN.PRE_LAUNCH import APP_INIT

from MODS.MAIN_STRORAGE_BI.pack_core.SHOWCASE.constructor import \
    test_processing_post_create, test_processing_delete, test_get_metadata

import asyncio
if __name__ == '__main__':
    ioloop = asyncio.get_event_loop()
    ioloop.run_until_complete(test_processing_post_create())
    # ioloop.run_until_complete(test_processing_delete())
    # ioloop.run_until_complete(test_get_metadata())