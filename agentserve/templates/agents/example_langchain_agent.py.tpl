from agentserve import Agent
from langchain import OpenAI

class ExampleAgent(Agent):
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def process(self, task_data):
        prompt = task_data.get('prompt', '')
        response = self.client.Completion.create(
            engine="gpt-4o-mini",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
