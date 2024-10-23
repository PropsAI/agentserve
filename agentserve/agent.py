# agentserve/agent.py
from typing import Dict, Any

class Agent:
    def process(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        User-defined method to process the incoming task data.
        Must be overridden by the subclass.
        """
        raise NotImplementedError("The process method must be implemented by the Agent subclass.")
