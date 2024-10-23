# agentserve/worker.py

import os
from redis import Redis
from rq import Worker, Queue, Connection

def run_worker():
    redis_host = os.getenv('REDIS_HOST', 'redis')
    redis_port = int(os.getenv('REDIS_PORT', 6379))
    redis_conn = Redis(host=redis_host, port=redis_port)
    with Connection(redis_conn):
        worker = Worker(Queue())
        worker.work()