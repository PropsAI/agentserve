from agentserve import Agent, AgentInput
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader
import os

class ExampleInput(AgentInput):
    query: str

class ExampleAgent(Agent):
    input_schema = ExampleInput
    
    def process(self, task_data):
        # Load documents from a directory
        documents = SimpleDirectoryReader('data').load_data()

        # Create an index from the documents
        index = GPTSimpleVectorIndex(documents)

        # Process the task data
        query = task_data.get('query', '')
        response = index.query(query)

        return response

