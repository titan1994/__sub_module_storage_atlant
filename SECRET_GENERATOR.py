"""
Помощник в формировании секретов для кубера
Кодирует в base64
"""

from json import dump as jsd
from MODS.scripts.python.process_base64 import data_to_base64_to_str

secrets = {
    'PYTHONPATH': '/jsonb_service',
    'PYTHONPATH1': '/__sub_module_storage_atlant',
    'DATABASE_SETTINGS_URL_DOCKER': 'postgresql://__test_app_core:__test_app_core@10.97.183.32:5432/__test_app_core',
    'JAVA_KEY_VALUE_JSONB_URL': 'http://jsonb-service:5112/structure/',
    'CLICKHOUSE_SHOWCASE_URL_DOCKER': 'clickhouse://default:@clickhouse:9000/default',
    'KAFKA_URL_DOCKER': 'kafka-bit:9092',
    'SECRET_KEY': 'boFsk9ie1l_E8PgWBbUrSSwLxEgxCwkZhSnsEtxjjAg=5PL31k5DXXuGYzmLyZWQ5rK-s549Z1dE371OufEcH3w='
}



result = {}
for name, val in secrets.items():
    data_secret = data_to_base64_to_str(val.encode())
    result[name] = data_secret

with open('SECRET_BASE64.json', 'w', encoding='utf-8') as fb:
    jsd(result, fb, ensure_ascii=False, indent=4)
