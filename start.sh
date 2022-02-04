gunicorn \
    -k uvicorn.workers.UvicornWorker \
    -w 2 \
    -b 0.0.0.0:33333 \
    -t 360 \
    app.main:app \
& \
gunicorn \
    -k uvicorn.workers.UvicornWorker \
    -w 2 \
    --certfile fullchain.pem \
    --keyfile privkey.pem \
    -b 0.0.0.0:44444 \
    -t 360 \
    app.main:app 