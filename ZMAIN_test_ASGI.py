"""
Запуск ASGI сервера - исключительно с целью тестирования.
В продуктиве всё через консоль
"""

if __name__ == '__main__':

    from pack_core.RUN.PRE_LAUNCH import pre_launch

    pre_launch()

    from GENERAL_CONFIG import GeneralConfig, FastApiConfig
    from os import system
    from sys import platform

    if FastApiConfig in GeneralConfig.__bases__:
        # FAST API - UVICORN

        if platform in ('win32', 'win64'):
            cmd = f'uvicorn --host 0.0.0.0 --port {GeneralConfig.DEFAULT_PORT} ' + \
                  f'--workers {GeneralConfig.DEFAULT_WORKER_COUNT} ZMAIN:app'

        else:
            cmd = f'gunicorn -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:{GeneralConfig.DEFAULT_PORT}' + \
                  f'-w {GeneralConfig.DEFAULT_WORKER_COUNT} ZMAIN:app'

    system(cmd)
