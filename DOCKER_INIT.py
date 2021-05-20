"""
Авто-генератор докер-файла и докер-композа
Настраивать через RENDER_DOCKERFILE

Скрипт предполагается запускать отсюда.
Если нужно просто что-то поделать с докер-файлами или композами, то:
AUTO_GENERATE_DOCKER = False
"""

from os import system, remove
from yaml import load as yml_load, FullLoader
from uuid import uuid4

from MODS.scripts.python.jinja import jinja_render_to_file

from GENERAL_CONFIG import GeneralConfig, FastApiConfig

# Auto create file (docker-compose.yml, Dockerfile)
AUTO_GENERATE_DOCKER = True

# General file path
GENERAL_DOCKER_COMPOSE = GeneralConfig.PROJECT_GENERAL_FOLDER / 'docker-compose.yml'
GENERAL_DOCKERFILE = GeneralConfig.PROJECT_GENERAL_FOLDER / 'Dockerfile'
GENERAL_ENV_DEV = GeneralConfig.PROJECT_GENERAL_FOLDER / '.env.development'
GENERAL_NGINX_CONF = GeneralConfig.PROJECT_GENERAL_FOLDER / '__docker' / 'volumes' / 'nginx' / 'nginx.conf'
GENERAL_PATH_REQUIREMENTS = 'pipenv lock -r > requirements.txt'

# JINJA2 pattern
GENERAL_PATH_JINJA_DOCKERFILE = GeneralConfig.PROJECT_GENERAL_FOLDER / '__docker' / 'pattern' / 'jinja_docker_file'
GENERAL_PATH_JINJA_DOCKER_COMPOSE = GeneralConfig.PROJECT_GENERAL_FOLDER / '__docker' / 'pattern' / 'jinja_docker_compose'
GENERAL_PATH_JINJA_ENV_DEV = GeneralConfig.PROJECT_GENERAL_FOLDER / '__docker' / 'pattern' / 'jinja_env'
GENERAL_PATH_JINJA_NGINX = GeneralConfig.PROJECT_GENERAL_FOLDER / '__docker' / 'pattern' / 'jinja_nginx_conf'


def get_command_to_run(windows_alternative=False):
    """
    Выбор команды запуска докер-файла, в зависимости от фреймворка

    Докер образы собираются для линукса (если требуется виндовский подход windows_alternative = True)
    Тоесть как тестировали - так и деплоим. Вцелом смысла в этом нет. uvloop точно быстрее asyncio
    """

    if FastApiConfig in GeneralConfig.__bases__:
        # FAST API - UVICORN

        if windows_alternative:
            command = f'CMD python PRE_LAUNCH.py && uvicorn --host 0.0.0.0 --port {GeneralConfig.DEFAULT_PORT} ' + \
                      f'--workers {GeneralConfig.DEFAULT_WORKER_COUNT} ZMAIN:app --reload'

        else:
            # Для конфигурации, совместимой с PyPy, используйте uvicorn.workers.UvicornH11Worker
            command = f'CMD python PRE_LAUNCH.py && gunicorn -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:{GeneralConfig.DEFAULT_PORT} ' + \
                      f'-w {GeneralConfig.DEFAULT_WORKER_COUNT} ZMAIN:app --reload'

    return command


RENDER_DOCKERFILE = {
    # Docker-Compose(only)
    'guid': f'_{uuid4()}',  # уникальный гуид для проекта
    'use_postgres': True,  # использовать постгрес
    'use_ycl': True,  # использовать кликхаус
    'use_nginx': False,  # использовать Nginx
    'use_kafka': True,  # использовать Кафку

    # External network
    'ext_ntw': 'general_network_all_services',  # имя внешней подсети
    # 'ext_ntw': False,

    # Nginx conf (if use_nginx: True)
    'worker_processes': GeneralConfig.DEFAULT_WORKER_COUNT,
    'worker_connections': 4096,
    'max_fails': 3,
    'fail_timeout': '60s',

    # Волюмы
    'project_folders': [
        {'name': '__migrations', 'comment': 'Миграции основного сервиса'},
        {'name': '__fast_api_app', 'comment': 'Основная обвязка реста'},
        {'name': 'data_launch_system', 'comment': 'Предпусковая настройка клиента'},
        {'name': 'MODS', 'comment': 'Модули'},
    ],

    # Docker-File(only)
    'cmd_run': get_command_to_run(),
    'requirements': GENERAL_PATH_REQUIREMENTS,

    # Основная папка проекта
    'core_folder': GeneralConfig.PROJECT_GENERAL_FOLDER.name,

    # Порт приложения
    'port_core': GeneralConfig.DEFAULT_PORT,
}


def python_generate_requirements():
    """
    Библиотеки - файл requirements.txt
    :return:
    """

    path_req = GeneralConfig.PROJECT_GENERAL_FOLDER / f'{GENERAL_PATH_REQUIREMENTS}.txt'

    if path_req.exists():
        remove(path_req.absolute())

    try:
        system(f'pipenv lock -r > {path_req.absolute()}')
    except Exception as exp:
        print(exp)
        return

    # Очистка файла от мусора
    with open(path_req, 'r') as f:
        data_req = f.readlines()

    with open(path_req, 'w') as f:
        f.writelines(data_req[:-1])


def docker_compose_get_all_external_volumes(file_yml):
    """
    Получить список всех внешних волюмов докера из yml файла
    :param file_yml:
    :return:
    """
    list_volumes = []
    with open(file_yml) as file:
        docker_dict = yml_load(file, Loader=FullLoader)
        if docker_dict.get('volumes'):
            for volume, prop in docker_dict['volumes'].items():
                if prop.get('external') and prop['external']:
                    list_volumes.append(volume)

    return list_volumes


def docker_generate_volume(volume_name):
    """
    Генератор внешних волюмов

    :param volume_name:
    :return:
    """

    try:
        system(f'docker volume create {volume_name}')
    except Exception as exp:
        print(exp)


def docker_compose_get_all_external_networks(file_yml):
    """
    Получить список всех внешних волюмов докера из yml файла
    :param file_yml:
    :return:
    """
    list_nws = []
    with open(file_yml) as file:
        docker_dict = yml_load(file, Loader=FullLoader)
        if docker_dict.get('networks'):
            for volume, prop in docker_dict['networks'].items():
                if prop.get('external') and prop['external']:
                    list_nws.append(volume)

    return list_nws


def docker_generate_network(network_name):
    """
    Генератор внешних сетей

    :param network_name:
    :return:
    """

    try:
        system(f'docker network create -d bridge {network_name}')
    except Exception as exp:
        print(exp)


def generate_docker_file():
    """
    Автогенератор докер-файла по конфигу. JINJA2
    :return:
    """

    jinja_render_to_file(
        GENERAL_PATH_JINJA_DOCKERFILE,
        GENERAL_DOCKERFILE,
        RENDER_DOCKERFILE
    )


def generate_docker_compose():
    """
    Автогенератор докер-композа по конфигу. JINJA2
    :return:
    """
    jinja_render_to_file(
        GENERAL_PATH_JINJA_DOCKER_COMPOSE,
        GENERAL_DOCKER_COMPOSE,
        RENDER_DOCKERFILE
    )


def generate_dev_env():
    """
    Авто-генератор переменных среды для докера
    :return:
    """
    new_render = {
        'core_folder': RENDER_DOCKERFILE['core_folder'],
        'db_path': 'postgresql://__test_app_core:__test_app_core@general_postgres:5432/__test_app_core'
    }

    # Берём настройки базы данных из композа
    core_folder = RENDER_DOCKERFILE['core_folder']
    guid = RENDER_DOCKERFILE['guid']
    name_psql_container = f'{core_folder}{guid}_postgres'

    with open(GENERAL_DOCKER_COMPOSE) as file:
        docker_dict = yml_load(file, Loader=FullLoader)
        psql_settings = docker_dict['services'].get(name_psql_container)

        if psql_settings:
            environment_psql = psql_settings.get('environment')
            if environment_psql:
                user = environment_psql['POSTGRES_USER']
                pswd = environment_psql['POSTGRES_PASSWORD']
                db = environment_psql['POSTGRES_DB']
                port = psql_settings['ports'][0][:4]

                new_render['db_path'] = f'postgresql://{user}:{pswd}@{name_psql_container}:{port}/{db}'

    jinja_render_to_file(
        GENERAL_PATH_JINJA_ENV_DEV,
        GENERAL_ENV_DEV,
        new_render
    )


def generate_nginx_conf():
    """
    Автогенератор nginx по конфигу. JINJA2
    :return:
    """

    jinja_render_to_file(
        GENERAL_PATH_JINJA_NGINX,
        GENERAL_NGINX_CONF,
        RENDER_DOCKERFILE
    )


if __name__ == '__main__':

    # requirements.txt
    python_generate_requirements()

    if AUTO_GENERATE_DOCKER:
        # docker_file
        generate_docker_file()

        # docker_compose
        generate_docker_compose()

        # env
        generate_dev_env()

    # генератор внешних волюмов по композу
    list_ext_volumes = docker_compose_get_all_external_volumes(GENERAL_DOCKER_COMPOSE)
    for volume in list_ext_volumes:
        docker_generate_volume(volume)

    # генератор внешних подсетей по композу
    # list_ext_networks = docker_compose_get_all_external_networks(GENERAL_DOCKER_COMPOSE)
    # for nwk in list_ext_networks:
    #     docker_generate_network(nwk)
