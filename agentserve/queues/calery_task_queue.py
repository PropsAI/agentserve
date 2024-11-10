# agentserve/celery_task_queue.py

import asyncio
from typing import Any, Dict
from .task_queue import TaskQueue
from ..config import Config
from ..logging_config import setup_logger

class CeleryTaskQueue(TaskQueue):
    def __init__(self, config: Config):
        try:
            from celery import Celery
        except ImportError:
            raise ImportError("CeleryTaskQueue requires the 'celery' package. Please install it.")

        self.logger = setup_logger("agentserve.queue.celery")
        broker_url = config.get('celery', {}).get('broker_url', 'pyamqp://guest@localhost//')
        self.celery_app = Celery('agent_server', broker=broker_url)
        self.loop = asyncio.new_event_loop()
        self._register_tasks()
        self.logger.info("CeleryTaskQueue initialized")

    def _register_tasks(self):
        @self.celery_app.task(name='agent_task')
        def agent_task(task_data, is_async=False):
            from ..agent_registry import AgentRegistry
            agent_registry = AgentRegistry()
            agent_function = agent_registry.get_agent()
            
            if is_async:
                asyncio.set_event_loop(self.loop)
                return self.loop.run_until_complete(agent_function(task_data))
            return agent_function(task_data)

    def enqueue(self, agent_function, task_data: Dict[str, Any], task_id: str):
        self.logger.debug(f"Enqueueing task {task_id}")
        is_async = getattr(agent_function, '_is_async', False)
        self.celery_app.send_task('agent_task', 
                                args=[task_data], 
                                kwargs={'is_async': is_async}, 
                                task_id=task_id)

    def get_status(self, task_id: str) -> str:
        result = self.celery_app.AsyncResult(task_id)
        return result.status

    def get_result(self, task_id: str) -> Any:
        result = self.celery_app.AsyncResult(task_id)
        if result.state == 'SUCCESS':
            return result.result
        if result.state == 'FAILURE':
            raise Exception(str(result.result))
        return None