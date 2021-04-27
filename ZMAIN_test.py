"""
Однопоточный запуск приложения (для тестов)
"""

if __name__ == "__main__":
    # Для тестов

    from pack_core.RUN.PRE_LAUNCH import pre_launch
    pre_launch()

    from pack_core.back_core import app
    from GENERAL_CONFIG import GeneralConfig, FastApiConfig

    if FastApiConfig in GeneralConfig.__bases__:
        import uvicorn
        uvicorn.run(app, host='0.0.0.0', port = GeneralConfig.DEFAULT_PORT)


