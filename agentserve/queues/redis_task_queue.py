# agentserve/redis_task_queue.py

import asyncio
from typing import Any, Dict
from .task_queue import TaskQueue
from ..logging_config import setup_logger

class RedisTaskQueue(TaskQueue):
    def __init__(self, config: Config):
        try:
            from redis import Redis
            from rq import Queue
        except ImportError:
            raise ImportError("RedisTaskQueue requires 'redis' and 'rq' packages. Please install them.")
        
        self.logger = setup_logger("agentserve.queue.redis")
        redis_config = config.get('redis', {})
        redis_host = redis_config.get('host', 'localhost')
        redis_port = redis_config.get('port', 6379)
        self.redis_conn = Redis(host=redis_host, port=redis_port)
        self.task_queue = Queue(connection=self.redis_conn)
        self.loop = asyncio.new_event_loop()
        self.logger.info("RedisTaskQueue initialized")
    
    def enqueue(self, agent_function, task_data: Dict[str, Any], task_id: str):
        self.logger.debug(f"Enqueueing task {task_id}")
        if getattr(agent_function, '_is_async', False):
            wrapped_func = self._wrap_async_function(agent_function)
            self.task_queue.enqueue_call(func=wrapped_func, args=(task_data,), job_id=task_id)
        else:
            self.task_queue.enqueue_call(func=agent_function, args=(task_data,), job_id=task_id)
    
    def _wrap_async_function(self, func):
        def wrapper(task_data):
            asyncio.set_event_loop(self.loop)
            return self.loop.run_until_complete(func(task_data))
        return wrapper
    
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