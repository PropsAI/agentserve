# agentserve/agent.py
from typing import Dict, Any, Type
from pydantic import BaseModel

class AgentInput(BaseModel):
    """Base class for defining agent input schemas. This is just an alias for BaseModel."""
    pass

class Agent:
    input_schema: Type[AgentInput] = AgentInput
    
    def _process(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        # Validate task_data against input_schema
        validated_data = self.input_schema(**task_data).dict()
        return self.process(validated_data)
    
    def process(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        User-defined method to process the incoming task data.
        Must be overridden by the subclass.
        """
        raise NotImplementedError("The process method must be implemented by the Agent subclass.")
