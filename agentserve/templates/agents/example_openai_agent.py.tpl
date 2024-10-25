from agentserve import Agent, AgentInput
from openai import OpenAI

class ExampleInput(AgentInput):
    prompt: str

class ExampleAgent(Agent):
    input_schema = ExampleInput
    
    def process(self, task_data):
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": task_data["prompt"]}],
        )
        return response.choices[0].message.content
