# agentserve/agent_registry.py
from typing import Callable, Optional, Type
from pydantic import BaseModel

class AgentRegistry:
    def __init__(self):
        self.agent_function = None
        self.input_schema: Optional[Type[BaseModel]] = None

    def register_agent(self, func: Optional[Callable] = None, *, input_schema: Optional[Type[BaseModel]] = None):
        if func is None:
            # Decorator is called with arguments
            def wrapper(func: Callable):
                return self.register_agent(func, input_schema=input_schema)
            return wrapper

        self.input_schema = input_schema

        def validated_func(task_data):
            if self.input_schema is not None:
                validated_data = self.input_schema(**task_data)
                return func(validated_data)
            else:
                return func(task_data)

        self.agent_function = validated_func
        return validated_func

    def get_agent(self):
        if self.agent_function is None:
            raise ValueError("No agent has been registered.")
        return self.agent_function