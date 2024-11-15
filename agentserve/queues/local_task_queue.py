# agentserve/local_task_queue.py

import asyncio
from typing import Any, Dict, Optional
from .task_queue import TaskQueue
import threading
from ..logging_config import setup_logger
import concurrent.futures

class LocalTaskQueue(TaskQueue):
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.logger = setup_logger("agentserve.queue.local")
        self.results = {}
        self.statuses = {}
        max_workers = 10  # default
        if config:
            max_workers = config.get('queue', {}).get('max_workers', 10)
        self.thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        self.lock = threading.Lock()
        self.logger.info("LocalTaskQueue initialized")

    def enqueue(self, agent_function, task_data: Dict[str, Any], task_id: str):
        self.logger.debug(f"Enqueueing task {task_id}")
        with self.lock:
            self.statuses[task_id] = 'queued'
        self.thread_pool.submit(self._run_task, agent_function, task_data, task_id)

    def _run_task(self, agent_function, task_data: Dict[str, Any], task_id: str):
        self.logger.debug(f"Starting task {task_id}")
        with self.lock:
            self.statuses[task_id] = 'in_progress'
        
        try:
            if getattr(agent_function, '_is_async', False):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    result = loop.run_until_complete(agent_function(task_data))
                finally:
                    loop.close()
            else:
                result = agent_function(task_data)
            
            with self.lock:
                self.results[task_id] = result
                self.statuses[task_id] = 'completed'
            self.logger.info(f"Task {task_id} completed successfully")
        
        except Exception as e:
            self.logger.error(f"Task {task_id} failed: {str(e)}")
            with self.lock:
                self.results[task_id] = e
                self.statuses[task_id] = 'failed'

    def get_status(self, task_id: str) -> str:
        with self.lock:
            return self.statuses.get(task_id, 'not_found')

    def get_result(self, task_id: str) -> Any:
        with self.lock:
            if task_id not in self.results:
                return None
            result = self.results[task_id]
            if isinstance(result, Exception):
                raise result
            return result