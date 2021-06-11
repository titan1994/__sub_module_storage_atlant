# Работа с манифестом

## Шаг 1 - пример пода, манифест

```
kubectl apply -f C:\Users\i.kozlov.CORP\Desktop\PyPro\K8sGitlabExampleCICD\k8s\simple_pods_v1.yaml
kubectl delete -f C:\Users\i.kozlov.CORP\Desktop\PyPro\K8sGitlabExampleCICD\k8s\simple_pods_v1.yaml

kubectl get pods
kubectl describe pods my-web

kubectl port-forward my-web 7788:80
```

## Шаг 2 - пример деплоя - консоль

Создание деплоя, анализ, скейлинг и автоскейлинг

```
kubectl create deployment depweb --image=adv4000/k8sphp:latest 

kubectl get deploy
kubectl get pods
kubectl describe pods depweb-55d8f44446-cnw2h 
kubectl describe deploy depweb

kubectl scale deployment depweb --replicas 4
kubectl get rs

kubectl autoscale deployment depweb --min=4 --max=6 --cpu-percent=80
kubectl get hpa
```

## Шаг 3 - апдейт image деплоя - консоль

Анализ истории изменений. Установка нового образа в контейнер деплоя. Ещё раз новый образ. Анализ истории. Откат
обратно. Откат на выбранную Обновление последнего базового образа

```
kubectl rollout history deployment depweb 
kubectl rollout status deployment depweb 

kubectl describe deploy depweb

kubectl set image deployment/depweb k8sphp=adv4000/k8sphp:version1 --record
kubectl rollout status deployment depweb 

kubectl set image deployment/depweb k8sphp=adv4000/k8sphp:version2 --record
kubectl rollout status deployment depweb 

kubectl rollout history deployment depweb 

--Откат назад
kubectl rollout undo deployment/depweb 

--Откат назад на выбранную
kubectl rollout undo deployment/depweb --to-revision=3

--Обновить латест :latest
kubectl rollout restart deployment/depweb 

kubectl delete deployment depweb 
```

## Шаг 4 - пример деплоя - файл

В файле автоскейлинг

```
kubectl apply -f C:\Users\i.kozlov.CORP\Desktop\PyPro\K8sGitlabExampleCICD\k8s\simple_deployment_v1.yaml
kubectl delete deployment depweb 
kubectl delete hpa --all
```

## Шаг 5 - сервис servises. Консоль

Ну сначала нужен деплой и только потом мы его превращаем в сервис

```
kubectl apply -f C:\Users\i.kozlov.CORP\Desktop\PyPro\K8sGitlabExampleCICD\k8s\simple_deployment_v1.yaml

--Доступный внутри кластера. И только так
kubectl expose deployment depweb --type=ClusterIP --port 80
kubectl get svc
kubectl delete service depweb

--Открытый по порту через ноду. Можно достучаться, зная IP Ноды и порт сервиса 
kubectl expose deployment depweb --type=NodePort --port 80
kubectl get svc
kubectl delete service depweb

--Открытый лоадбалансер. Балансировщик облачной нагрузки. Локально(миникуб) свои тараканы
kubectl expose deployment depweb --type=LoadBalancer --port 80

minikube service depweb --url   в миникубе, эта команда фактически запускает сервис
minikube service depweb

kubectl describe services depweb

kubectl delete -f C:\Users\i.kozlov.CORP\Desktop\PyPro\K8sGitlabExampleCICD\k8s\simple_deployment_v1.yaml
kubectl delete service depweb
```

# Шаг 6 - сервис через манифест с лоадбалансером

```
kubectl apply -f C:\Users\i.kozlov.CORP\Desktop\PyPro\K8sGitlabExampleCICD\k8s\simple_service_v1.yaml
minikube service depweb

kubectl delete -f C:\Users\i.kozlov.CORP\Desktop\PyPro\K8sGitlabExampleCICD\k8s\simple_service_v1.yaml
```

# Шаг 7 - Ингрес контроллер.

Для начала необходимо выбрать нужный и задеплоить его

https://docs.google.com/spreadsheets/d/191WWNpjJ2za6-nbG4ZoUMXMpUK8KlCIosvQB0f-oq3k/edit#gid=907731238

Пример:

https://github.com/adv4000/k8s-lessons/tree/master/Lesson-11-Ingress

Видос:

https://www.youtube.com/watch?v=ThP-OEjpDZk&list=PLg5SS_4L6LYvN1RqaVesof8KAf-02fJSi&index=11

Попытки собрать - ни к чему не привели. Локально не работает на винде

```
kubectl apply -f https://projectcontour.io/quickstart/contour.yaml

kubectl get svc -n projectcontour

kubectl apply -f C:\Users\i.kozlov.CORP\Desktop\PyPro\K8sGitlabExampleCICD\k8s\simple_ingress_v1.yaml
kubectl get ingress
minikube ip
```

# Шаг 8 - Хэлм чарт.

Пример:

https://github.com/adv4000/k8s-lessons/tree/master/Lesson-12-HelmCharts

Видос:

https://www.youtube.com/watch?v=-lLT0vlaBpk&list=PLg5SS_4L6LYvN1RqaVesof8KAf-02fJSi&index=12

Деплой по умолчанию, деплой с подстановкой переменных из файла

```
helm install app C:\Users\i.kozlov.CORP\Desktop\PyPro\K8sGitlabExampleCICD\k8s\simple_helm\
minikube service app-depweb

helm install app2 C:\Users\i.kozlov.CORP\Desktop\PyPro\K8sGitlabExampleCICD\k8s\simple_helm\ -f C:\Users\i.kozlov.CORP\Desktop\PyPro\K8sGitlabExampleCICD\k8s\simple_helm\prod_values.yaml
minikube service app2-depweb

```

# Шаг 9 - Осознание того, что чартов велкиое множество, как образов на докерхабе

Чтобы с ними работать - надо добавлять их к себе в репозиторий

``` 
helm repo add bitnami https://charts.bitnami.com/bitnami
helm search repo bitnami

helm install web-apache bitnami/apache 
```

# Шаг 10 - Осознание того, что композ можно конвертировать в кубер!

https://kubernetes.io/docs/tasks/configure-pod-container/translate-compose-kubernetes/

``` 
curl -L https://github.com/kubernetes/kompose/releases/download/v1.22.0/kompose-windows-amd64.exe -o kompose.exe

kompose convert
``` 

Минусы - конвертирует в поды


МЕГА ЖЕСТЬ - КОНВЕРТИРУЕТ И ЗАПУСКАЕТ, не сработало. У нас сложный композ
``` 
kompose up
``` 