# agentserve/task_queue.py

from abc import ABC, abstractmethod
from typing import Any, Dict

class TaskQueue(ABC):
    @abstractmethod
    def enqueue(self, agent_function, task_data: Dict[str, Any], task_id: str):
        pass

    @abstractmethod
    def get_status(self, task_id: str) -> str:
        pass

    @abstractmethod
    def get_result(self, task_id: str) -> Any:
        pass