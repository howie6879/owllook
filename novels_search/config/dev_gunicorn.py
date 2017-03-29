# gunicorn config
# gunicorn -c config/dev_gunicorn.py --worker-class sanic_gunicorn.Worker server:app
bind = '0.0.0.0:8000'
backlog = 2048

workers = 1
worker_connections = 1000
timeout = 30
keepalive = 2

spew = False
daemon = False
umask = 0
