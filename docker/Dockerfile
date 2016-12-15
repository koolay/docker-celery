FROM python:2.7.12-alpine

RUN addgroup -S celery && adduser -S -G celery celery
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apk add --no-cache build-base
ENV TZ=Asia/Shanghai APP_PATH=/app  APP_NAME=myproj LOG_LEVEL=INFO  CONCURRENCY=5

COPY run.sh /celery.sh
COPY requirement.txt $APP_PATH/requirement.txt
RUN chmod +x /celery.sh \
    && pip install -r $APP_PATH/requirement.txt

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apk del build-base
RUN mkdir $APP_PATH && chown celery:celery $APP_PATH
VOLUME ["/app"]
WORKDIR $APP_PATH
USER celery
ENTRYPOINT ["/celery.sh"]
