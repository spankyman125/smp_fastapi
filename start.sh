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
    --certfile /etc/letsencrypt/live/septerra.duckdns.org/fullchain.pem \
    --keyfile /etc/letsencrypt/live/septerra.duckdns.org/privkey.pem \
    -b 0.0.0.0:44444 \
    -t 360 \
    app.main:app 