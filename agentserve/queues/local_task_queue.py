# agentserve/local_task_queue.py

import asyncio
from typing import Any, Dict
from .task_queue import TaskQueue
import threading

class LocalTaskQueue(TaskQueue):
    def __init__(self):
        self.results = {}
        self.statuses = {}
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self._run_event_loop, daemon=True)
        self.thread.start()

    def _run_event_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def enqueue(self, agent_function, task_data: Dict[str, Any], task_id: str):
        self.statuses[task_id] = 'queued'
        asyncio.run_coroutine_threadsafe(
            self._run_task(agent_function, task_data, task_id),
            self.loop
        )

    async def _run_task(self, agent_function, task_data: Dict[str, Any], task_id: str):
        self.statuses[task_id] = 'in_progress'
        try:
            result = await agent_function(task_data)
            self.results[task_id] = result
            self.statuses[task_id] = 'completed'
        except Exception as e:
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
