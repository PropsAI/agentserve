import agentserve
from pydantic import BaseModel
import asyncio

# Configure logging level
agentserve.setup_logger(level="DEBUG")  # or "INFO", "WARNING", "ERROR"

app = agentserve.app()

class MyInputSchema(BaseModel):
    prompt: str

@app.agent(input_schema=MyInputSchema)
async def my_agent(task_data):
    await asyncio.sleep(20)
    return task_data

app.run()