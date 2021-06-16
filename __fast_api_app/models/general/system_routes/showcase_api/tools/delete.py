from GENERAL_CONFIG import GeneralConfig
from MODS.DRIVERS.data_base.async_click_house.ycl import delete_data_from_table
from MODS.storage_atlant_driver.pack_core.main import ycl_get_connection_settings
from .settings import get_showcase_data


async def showcase_delete_base(client_key, showcase_name, filter_data):
    """
    Функция для удаления данных из витрины.
    Получает название таблицы.
    Создаёт коннект.
    Посылает запрос на удаление.
    """
    meta_data = await get_showcase_data(client_key, showcase_name)
    table = meta_data['target_table']['table_name']
    conn = ycl_get_connection_settings(GeneralConfig.CLICKHOUSE_SHOWCASE_URL)
    res = await delete_data_from_table(conn, table, filter_data)
    return res


