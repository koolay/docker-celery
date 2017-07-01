Celery queue
-----------

## deploy worker

`celery -A snh worker --loglevel=info --concurrency=4 -n worker@%h`

- docker

```bash

docker run --name myCeleryWorker --restart=always \
    -e APP_NAME=app -e CONCURRENCY=5 \
    --env-file /home/koolay/approot/.env \
    -v /home/koolay/approot:/app \
    --link redis \
    daocloud.io/koolay/celery:latest

```

## nodejs client

- queue.js

```javascript

var celery = require('node-celery')

module.exports = {

  /*
   * enque
   * @param queName string
   * @param args array
   * @param cb function
   */
    enque: function (queName, args, cb) {
        var client = celery.createClient({
            CELERY_BROKER_URL: 'redis://127.0.0.1:6379/0'
        })

        client.on('error', function (err) {
            console.log(err)
            throw err
        })

        client.on('connect', function (argument) {
            console.log(args)
            client.call(queName, args, function (result) {
                client.end()
                if (cb) {
                    cb(result)
                }
            })
        })
    }
}

```
- call

```
var queue = require('./queue')

queue.enque('push.push_message_to_user',
    [ 
      123,
      'Hello,celery!',
      6
    ], result => {
        console.log(result)
    })

```

