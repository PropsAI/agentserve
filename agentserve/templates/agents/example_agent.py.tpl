from agentserve import Agent, AgentInput

class ExampleInput(AgentInput):
    prompt: str

class ExampleAgent(Agent):
    input_schema = ExampleInput
    def process(self, task_data):
        return ""

