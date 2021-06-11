# Важные команды

## Перезапуск миникубера
```
minikube delete
minikube start --cpus=4 --memory=8gb –disk-size=40gb --mount=true --mount-string=C:\Users\i.kozlov.CORP\Desktop\PyPro\__sub_module_storage_atlant\prod_k8s\volume:/data
```

## Подымаем дашборд - для мониторинга кластера

https://github.com/kubernetes/dashboard

```
kubectl apply -f C:\Users\i.kozlov.CORP\Desktop\PyPro\__sub_module_storage_atlant\prod_k8s\dashboard\dashboard-adminuser.yaml
kubectl -n kubernetes-dashboard get secret $(kubectl -n kubernetes-dashboard get sa/admin-user -o jsonpath="{.secrets[0].name}") -o go-template="{{.data.token | base64decode}}"
kubectl proxy
```

http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/

## Создание/удаление общего волюма
```
kubectl apply -f C:\Users\i.kozlov.CORP\Desktop\PyPro\__sub_module_storage_atlant\prod_k8s\raw\presistent_volumes.yaml
kubectl delete -f C:\Users\i.kozlov.CORP\Desktop\PyPro\__sub_module_storage_atlant\prod_k8s\raw\presistent_volumes.yaml
```


## Подымаем кафку и gui - включаем форвардинг - да всегда, да у нас нет полноценного кубера и ингреса
```
helm install kafka-bit bitnami/kafka
kubectl apply -f C:\Users\i.kozlov.CORP\Desktop\PyPro\__sub_module_storage_atlant\prod_k8s\raw\kafdrop.yaml
kubectl port-forward svc/kafdrop 9001:9001
```

## Подымаем постгрес и psql. Создаём претензию на волюм
```
kubectl apply -f C:\Users\i.kozlov.CORP\Desktop\PyPro\__sub_module_storage_atlant\prod_k8s\raw\psql_pvc.yaml

helm install psql bitnami/postgresql -f C:\Users\i.kozlov.CORP\Desktop\PyPro\__sub_module_storage_atlant\prod_k8s\raw\psql_values.yaml
kubectl apply -f C:\Users\i.kozlov.CORP\Desktop\PyPro\__sub_module_storage_atlant\prod_k8s\raw\dbviewer.yaml

kubectl port-forward svc/dbviewer 8978:8978
kubectl port-forward svc/psql-postgresql 5432:5432
```

## Подымаем хранилище метаданных JSONB
```
kubectl apply -f C:\Users\i.kozlov.CORP\Desktop\PyPro\__sub_module_storage_atlant\prod_k8s\raw\jsonb.yaml
kubectl delete -f C:\Users\i.kozlov.CORP\Desktop\PyPro\__sub_module_storage_atlant\prod_k8s\raw\jsonb.yaml
kubectl port-forward svc/jsonb-service 5112:5112
```


## Подымаем кликхаус
```
kubectl apply -f C:\Users\i.kozlov.CORP\Desktop\PyPro\__sub_module_storage_atlant\prod_k8s\raw\ycl_pvc.yaml
helm install clickhouse liwenhe/clickhouse -f C:\Users\i.kozlov.CORP\Desktop\PyPro\__sub_module_storage_atlant\prod_k8s\raw\ycl_values.yaml
helm delete clickhouse 
kubectl delete -f C:\Users\i.kozlov.CORP\Desktop\PyPro\__sub_module_storage_atlant\prod_k8s\raw\ycl_pvc.yaml
kubectl port-forward svc/clickhouse 9000:9000
kubectl port-forward svc/clickhouse 8123:8123
```

## Подымаем основной сервис Хранилище АТЛАНТ
```
kubectl apply -f C:\Users\i.kozlov.CORP\Desktop\PyPro\__sub_module_storage_atlant\prod_k8s\raw\storage_atlant.yaml
kubectl delete -f C:\Users\i.kozlov.CORP\Desktop\PyPro\__sub_module_storage_atlant\prod_k8s\raw\storage_atlant.yaml
kubectl port-forward svc/storage-atlant-service 5111:5111
```