#!/usr/bin/env python
"""
 Created by howie.hu at 2018/8/13.
"""
import os
import subprocess

if __name__ == '__main__':
    os.environ['MODE'] = 'PRO'
    servers = [
        ["pipenv", "run", "gunicorn", "-c", "config/gunicorn.py", "--worker-class", "sanic.worker.GunicornWorker",
         "server:app"],
        ["pipenv", "run", "python", "scheduled_task.py"]
    ]
    procs = []
    for server in servers:
        proc = subprocess.Popen(server)
        procs.append(proc)
    for proc in procs:
        proc.wait()
        if proc.poll():
            exit(0)
