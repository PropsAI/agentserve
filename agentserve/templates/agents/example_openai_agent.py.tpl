from agentserve import Agent
from openai import OpenAI

class ExampleAgent(Agent):
    def process(self, task_data: Dict[str, Any]):
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": task_data["prompt"]}],
        )
        return response.choices[0].message.content
