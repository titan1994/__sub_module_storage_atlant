FROM python:3.8

# Установка библиотек
RUN set -ex && mkdir -p /__sub_module_storage_atlant/
WORKDIR /__sub_module_storage_atlant/
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install tortoise-orm[accel]

# Копирование файлов запуска
WORKDIR /__sub_module_storage_atlant/
COPY ./GENERAL_CONFIG.py ./ZMAIN.py ./PRE_LAUNCH.py ./.gitignore ./


# Копировать. Миграции основного сервиса
RUN set -ex && mkdir -p /__sub_module_storage_atlant/__migrations/
WORKDIR /__sub_module_storage_atlant/__migrations/
COPY ./__migrations .

# Копировать. Тестовые данные
RUN set -ex && mkdir -p /__sub_module_storage_atlant/__test_data/
WORKDIR /__sub_module_storage_atlant/__test_data/
COPY ./__test_data .

# Копировать. Основная обвязка реста
RUN set -ex && mkdir -p /__sub_module_storage_atlant/__fast_api_app/
WORKDIR /__sub_module_storage_atlant/__fast_api_app/
COPY ./__fast_api_app .

# Копировать. Предпусковая настройка клиента
RUN set -ex && mkdir -p /__sub_module_storage_atlant/data_launch_system/
WORKDIR /__sub_module_storage_atlant/data_launch_system/
COPY ./data_launch_system .

# Копировать. Модули
RUN set -ex && mkdir -p /__sub_module_storage_atlant/MODS/
WORKDIR /__sub_module_storage_atlant/MODS/
COPY ./MODS .



# Открываем волюмы
VOLUME /__sub_module_storage_atlant/__migrations/ /__sub_module_storage_atlant/__fast_api_app/models/general/NSI/ /__sub_module_storage_atlant/data_launch_system/ /__sub_module_storage_atlant/__test_data/

# Открываем порт
EXPOSE 5111

# Команда запуска
WORKDIR /__sub_module_storage_atlant/
CMD python PRE_LAUNCH.py && gunicorn -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:5111 -w 9 ZMAIN:app --reload