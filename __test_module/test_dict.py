from MODS.rest_core.pack_core.RUN.PRE_LAUNCH import APP_INIT
from pack_core.NSI.tortoise_bridge import test_processing_post_create, test_processing_delete

import asyncio
if __name__ == '__main__':
    """
    Тест
    """

    ioloop = asyncio.get_event_loop()
    ioloop.run_until_complete(test_processing_post_create())
    # ioloop.run_until_complete(test_processing_delete())
