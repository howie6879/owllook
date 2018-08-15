# gunicorn config
import os

WORKERS = os.getenv('WORKERS', 2)
TIMEOUT = os.getenv('TIMEOUT', 60)

bind = '0.0.0.0:8001'
backlog = 2048

workers = WORKERS
worker_connections = 1000
keepalive = 2

spew = False
daemon = False
umask = 0
timeout = TIMEOUT
preload = True
