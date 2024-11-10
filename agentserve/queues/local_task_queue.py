# agentserve/local_task_queue.py

import asyncio
from typing import Any, Dict
from .task_queue import TaskQueue
import threading
from ..logging_config import setup_logger

class LocalTaskQueue(TaskQueue):
    def __init__(self):
        self.logger = setup_logger("agentserve.queue.local")
        self.results = {}
        self.statuses = {}
        self.loop = asyncio.new_event_loop()
        self.logger.info("LocalTaskQueue initialized")

    def enqueue(self, agent_function, task_data: Dict[str, Any], task_id: str):
        self.logger.debug(f"Enqueueing task {task_id}")
        self.statuses[task_id] = 'queued'
        threading.Thread(target=self._run_task, args=(agent_function, task_data, task_id)).start()

    def _run_task(self, agent_function, task_data: Dict[str, Any], task_id: str):
        self.logger.debug(f"Starting task {task_id}")
        self.statuses[task_id] = 'in_progress'
        try:
            if getattr(agent_function, '_is_async', False):
                asyncio.set_event_loop(self.loop)
                result = self.loop.run_until_complete(agent_function(task_data))
            else:
                result = agent_function(task_data)
            self.results[task_id] = result
            self.statuses[task_id] = 'completed'
            self.logger.info(f"Task {task_id} completed successfully")
        except Exception as e:
            self.logger.error(f"Task {task_id} failed: {str(e)}")
            self.results[task_id] = e
            self.statuses[task_id] = 'failed'

    def get_status(self, task_id: str) -> str:
        return self.statuses.get(task_id, 'not_found')

    def get_result(self, task_id: str) -> Any:
        if task_id not in self.results:
            return None
        result = self.results[task_id]
        if isinstance(result, Exception):
            raise result
        return result