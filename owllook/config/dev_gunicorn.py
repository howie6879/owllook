# gunicorn config
# gunicorn -c config/dev_gunicorn.py --worker-class sanic.worker.GunicornWorker server:app
import os

WORKERS = os.getenv('WORKERS', 1)


bind = '0.0.0.0:8001'
backlog = 2048

workers = WORKERS
worker_connections = 1000
timeout = 30
keepalive = 2

spew = False
daemon = False
umask = 0
preload = True
