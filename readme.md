# Универсальное хранилище

Хранилище это стек технологий: 
1. Кликхаус
2. Кафка
3. JSONB-Postgres
4. ORM Tortoise + Postgres

Хранилище состоит из витрины данных, и словарей к ней подключенных. 
Самый верхний узел - это клиент. 
У клиента может быть множество хранилищ-витрин данных со своими словарями

Обязательно идёт в комплект к рест-сервису на фаст-апи!

## Если очень хочется... 

То можно фаст-апи не запускать. Оставить только функционал аерика и миграций. 
Делается это просто, смотрите примеры в папке __test_module.
Эти примеры будут работать без фаст апи - если сделать просто Prelaunch 
именно инициализацию приложения, а не воркера
