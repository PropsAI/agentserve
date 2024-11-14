import agentserve
from pydantic import BaseModel

# Configure logging level
agentserve.setup_logger(level="INFO")  # or "INFO", "WARNING", "ERROR"

app = agentserve.app()


class MyInputSchema(BaseModel):
    prompt: str

@app.agent(input_schema=MyInputSchema)
def my_agent(task_data):
    return task_data

app.run()