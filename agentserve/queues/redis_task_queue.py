# agentserve/redis_task_queue.py

from typing import Any, Dict
from .task_queue import TaskQueue

class RedisTaskQueue(TaskQueue):
    def __init__(self, config: Config):
        try:
            from redis import Redis
            from rq import Queue
        except ImportError:
            raise ImportError("RedisTaskQueue requires 'redis' and 'rq' packages. Please install them.")
        
        redis_config = config.get('redis', {})
        redis_host = redis_config.get('host', 'localhost')
        redis_port = redis_config.get('port', 6379)
        self.redis_conn = Redis(host=redis_host, port=redis_port)
        self.task_queue = Queue(connection=self.redis_conn)
    
    def enqueue(self, agent_function, task_data: Dict[str, Any], task_id: str):
        self.task_queue.enqueue_call(func=agent_function, args=(task_data,), job_id=task_id)
    
    def get_status(self, task_id: str) -> str:
        job = self.task_queue.fetch_job(task_id)
        return job.get_status() if job else 'not_found'
    
    def get_result(self, task_id: str) -> Any:
        job = self.task_queue.fetch_job(task_id)
        if not job:
            return None
        if job.is_finished:
            return job.result
        if job.is_failed:
            raise Exception(job.exc_info)
        return None