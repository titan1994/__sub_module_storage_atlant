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