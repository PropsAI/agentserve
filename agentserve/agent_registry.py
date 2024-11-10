# agentserve/agent_registry.py
from typing import Callable, Optional, Type
from pydantic import BaseModel
from .logging_config import setup_logger
import asyncio

class AgentRegistry:
    def __init__(self):
        self.agent_function = None
        self.input_schema: Optional[Type[BaseModel]] = None
        self.logger = setup_logger("agentserve.agent_registry")
        
    def register_agent(self, func: Optional[Callable] = None, *, input_schema: Optional[Type[BaseModel]] = None):
        if func is None:
            def wrapper(func: Callable):
                return self.register_agent(func, input_schema=input_schema)
            return wrapper

        self.input_schema = input_schema
        is_async = asyncio.iscoroutinefunction(func)
        self.logger.info(f"Registering {'async' if is_async else 'sync'} function")

        async def async_validated_func(task_data):
            if self.input_schema is not None:
                validated_data = self.input_schema(**task_data)
                return await func(validated_data)
            return await func(task_data)

        def sync_validated_func(task_data):
            if self.input_schema is not None:
                validated_data = self.input_schema(**task_data)
                return func(validated_data)
            return func(task_data)

        if is_async:
            self.agent_function = async_validated_func
            setattr(self.agent_function, '_is_async', True)
        else:
            self.agent_function = sync_validated_func
            setattr(self.agent_function, '_is_async', False)

        return self.agent_function

    def get_agent(self):
        if self.agent_function is None:
            raise ValueError("No agent has been registered.")
        return self.agent_function