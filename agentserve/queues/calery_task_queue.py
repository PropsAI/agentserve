# agentserve/celery_task_queue.py

from typing import Any, Dict
from .task_queue import TaskQueue
from ..config import Config
class CeleryTaskQueue(TaskQueue):
    def __init__(self, config: Config):
        try:
            from celery import Celery
        except ImportError:
            raise ImportError("CeleryTaskQueue requires the 'celery' package. Please install it.")

        broker_url = config.get('celery', {}).get('broker_url', 'pyamqp://guest@localhost//')
        self.celery_app = Celery('agent_server', broker=broker_url)
        self._register_tasks()

    def _register_tasks(self):
        @self.celery_app.task(name='agent_task')
        def agent_task(task_data):
            from .agent_registry import AgentRegistry
            agent_registry = AgentRegistry()
            agent_function = agent_registry.get_agent()
            return agent_function(task_data)

    def enqueue(self, agent_function, task_data: Dict[str, Any], task_id: str):
        # Since the agent task is registered with Celery, we just send the task name
        self.celery_app.send_task('agent_task', args=[task_data], task_id=task_id)

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