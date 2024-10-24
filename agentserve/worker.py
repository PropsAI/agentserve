# agentserve/worker.py

import os
import logging
from redis import Redis
from rq import Worker, Queue, Connection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_worker():
    redis_host = os.getenv('REDIS_HOST', 'redis')
    redis_port = int(os.getenv('REDIS_PORT', 6379))
    logger.info(f"Connecting to Redis at {redis_host}:{redis_port}")
    
    try:
        redis_conn = Redis(host=redis_host, port=redis_port)
        redis_conn.ping()  # Test Redis connection
        logger.info("Successfully connected to Redis.")
    except Exception as e:
        logger.error(f"Error connecting to Redis: {e}")
        return

    with Connection(redis_conn):
        queues = [Queue()]  # default queue
        logger.info(f"Starting worker on queues: {[q.name for q in queues]}")
        worker = Worker(queues)
        
        try:
            worker.work()
        except Exception as e:
            logger.error(f"Worker encountered an error: {e}")
        finally:
            logger.info("Worker has stopped.")

if __name__ == '__main__':
    run_worker()
