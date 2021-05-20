Перед запуском докера необходимо создать волюм постгреса 
И общую сеть. Выполнив последовательно команды:

```
docker volume create psql_sub_module_storage_atlant
docker network create -d bridge general_network_all_services
```

