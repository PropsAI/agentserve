from agentserve import Agent, AgentInput
from langchain import OpenAI

class ExampleInput(AgentInput):
    prompt: str

class ExampleAgent(Agent):
    input_schema = ExampleInput
    
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
