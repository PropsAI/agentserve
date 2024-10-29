# agentserve/agent_registry.py

class AgentRegistry:
    def __init__(self):
        self._agent_function = None

    def register_agent(self, func):
        self._agent_function = func
        return func

    def get_agent(self):
        if not self._agent_function:
            raise Exception("No agent function registered")
        return self._agent_function