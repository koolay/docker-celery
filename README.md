
## docker

```

docker run --name myCeleryWorker --restart=always \
    -e APP_NAME=app -e CONCURRENCY=5 \
    --env-file /home/koolay/approot/.env \
    -v /home/koolay/approot:/app \
    --link redis \
    --link mongo \
    daocloud.io/koolay/celery:latest

```
