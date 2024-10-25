```
   ___                __  ____
  / _ |___ ____ ___  / /_/ __/__ _____  _____
 / __ / _ `/ -_) _ \/ __/\ \/ -_) __/ |/ / -_)
/_/ |_\_, /\__/_//_/\__/___/\__/_/  |___/\__/
     /___/
```

# AgentServe

[![GitHub](https://img.shields.io/badge/GitHub-View_on_GitHub-blue?style=flat&logo=GitHub)](https://github.com/PropsAI/agentserve)
![License](https://img.shields.io/badge/License-MIT-blue.svg)
![PyPI Version](https://img.shields.io/pypi/v/agentserve.svg)
![GitHub Stars](https://img.shields.io/github/stars/PropsAI/agentserve?style=social)


AgentServe is an SDK & CLI for hosting and managing AI agents. It provides a simple interface to wrap your agent in a FastAPI server with a Redis queue to maintain tasks. The output is a single docker image that you can deploy anywhere.

## Goals and Objectives

The goal of AgentServe is to provide the easiest way to take an local agent to production and standardize the communication layer between multiple agents, humans, and other systems.

## Features

- **Standardized:** AgentServe provides a standardized way to communicate with AI agents via a REST API.
- **Framework Agnostic:** AgentServe supports multiple agent frameworks (OpenAI, LangChain, LlamaIndex, and Blank).
- **Dockerized:** The output is a single docker image that you can deploy anywhere.
- **Easy to Use:** AgentServe provides a CLI tool to initialize and setup your AI agent projects.
- **Schema Validation:** Define input schemas for your agents using AgentInput to ensure data consistency and validation.

## Requirements

- Python 3.9+

## Installation

To install the AgentServe SDK, you can use pip:

```bash
pip install -U agentserve
```

## CLI Commands

AgentServe provides a Command-Line Interface (CLI) tool to setup your AI agent projects. Below are the available commands and their usages.

```bash
agentserve init <project_name> [--framework <framework>] # Initialize a new project
agentserve build # Generate Dockerfiles
agentserve run # Run the API server and worker
```

## Getting Started

First we need to set up agentserve in our project. We can do this by running the `init` command to create a new project.

### Initialize a New Project

Create a new AgentServe project with a specified agent framework (this will default to OpenAI, see [CLI Usage](#cli-usage) for more details).

```bash
agentserve init my_project
```

This command adds AgentServe to the current project using the OpenAI framework.

### Update Environment Variables

You can update the environment variables in the `.env` file to add your OpenAI API key.

### Build the Docker Image

```bash
agentserve build
```

### Run the Server

Use Docker Compose to build and run the server:

```bash
agentserve run
```

This command starts the API server and a Redis instance, allowing your agent to process tasks.

### Test the Agent

The agent will be running on `http://localhost:5618/` and have the following endpoint:

- `POST /task/sync` - Synchronously process a task
- `POST /task/async` - Asynchronously process a task
- `GET /task/status/:task_id` - Get the status of a task
- `GET /task/result/:task_id` - Get the result of a task

**Example:**

```bash
curl -X POST http://localhost:5618/task/sync -H "Content-Type: application/json" -d '{"prompt": "What is the capital of France?"}'
```

## Example Project Structure

After initializing a new project, your project directory will look like this:

```
my_project/
├── agents/
│   ├── example_agent.py
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
├── main.py
├── requirements.txt
├── .env
```

- **`main.py`**: The main application file where the agent server is configured.
- **`Dockerfile` & `docker-compose.yml`**: Docker configurations for building and running the application.
- **`example_agent.py`**: An example agent tailored to the OpenAI framework.
- **`requirements.txt`**: Lists Python dependencies.

## API Reference

### POST /task/sync

Synchronously process a task.

**Request Body:**

- `task_data`: A dictionary containing the task data.

**Response:**

- `result`: The result of the task.

### POST /task/async

Asynchronously process a task.

**Request Body:**

- `task_data`: A dictionary containing the task data.

**Response:**

- `task_id`: The ID of the task.

### GET /task/status/:task_id

Get the status of a task.

**Response:**

- `status`: The status of the task.

### GET /task/result/:task_id

Get the result of a task.

**Response:**

- `result`: The result of the task.

## Defining Input Schemas

AgentServe uses AgentInput (an alias for Pydantic's BaseModel) to define and validate the input schemas for your agents. This ensures that the data received by your agents adheres to the expected structure, enhancing reliability and developer experience.
### Subclassing AgentInput
To define a custom input schema for your agent, subclass AgentInput and specify the required fields.

**Example:**

```python
# agents/custom_agent.py
from agentserve.agent import Agent, AgentInput
from typing import Optional, Dict, Any

class CustomTaskSchema(AgentInput):
    input_text: str
    parameters: Optional[Dict[str, Any]] = None

class CustomAgent(Agent):
    input_schema = CustomTaskSchema

    def process(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        # Implement your processing logic here
        input_text = task_data["input_text"]
        parameters = task_data.get("parameters", {})
        # Example processing
        processed_text = input_text.upper()  # Simple example
        return {"processed_text": processed_text, "parameters": parameters}
```

### Updating Your Agent

When creating your agent, assign your custom schema to the input_schema attribute. This ensures that all incoming task_data is validated against your defined schema before processing.

**Steps:**

1. Define the Input Schema:

    ```python
    from agentserve.agent import Agent, AgentInput
    from typing import Optional, Dict, Any

    class MyTaskSchema(AgentInput):
        prompt: str
        settings: Optional[Dict[str, Any]] = None
    ```

2. Implement the Agent:

    ```python
    class MyAgent(Agent):
        input_schema = MyTaskSchema

        def process(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
            prompt = task_data["prompt"]
            settings = task_data.get("settings", {})
            # Your processing logic here
            response = {"response": f"Echo: {prompt}", "settings": settings}
            return response
    ```

### Handling Validation Errors

AgentServe will automatically validate incoming task_data against the defined input_schema. If the data does not conform to the schema, a 400 Bad Request error will be returned with details about the validation failure.

**Example Response:**

```json
{
  "detail": [
    {
      "loc": ["body", "prompt"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}   
```

Ensure that your clients provide data that matches the schema to avoid validation errors.

## CLI Usage

### Init Command (for new projects)

To create a new project with AgentServe:

```bash
agentserve init <project_name> [--framework <framework>]
```

**Options:**

- `--framework`: (Optional) Specify the type of agent framework to use. Available options:
  - `openai` (default)
  - `langchain`
  - `llamaindex`
  - `blank`

**Example:**

```bash
agentserve init my_new_project --framework openai
```

**Result:**

- Creates a new directory named `my_new_project`.
- Populates it with necessary AgentServe files tailored to the OpenAI framework.
- Sets up `requirements.txt` with necessary dependencies.

### Build Command

```bash
agentserve build
```

### Run Command

```bash
agentserve run
```

## Adding AgentServe to an Existing Project

This guide provides step-by-step instructions to manually integrate AgentServe into your existing Python application. By following these steps, you can add AI agent capabilities to your project without using the AgentServe CLI.

### Steps to Integrate AgentServe

#### 1. Install AgentServe

First, install the agentserve package using pip:

```bash
pip install agentserve
```

If you're using a virtual environment, make sure it is activated before running the command.

#### 2. Update Your requirements.txt

If your project uses a requirements.txt file, add agentserve to it:

```
agentserve
```

This ensures that AgentServe will be installed when setting up the project in the future.

#### 3. Create an agents Directory

Create a new directory called agents in the root of your project. This is where your agent classes will reside.

```bash
mkdir agents
```

#### 4. Implement Your Agent Class

Inside the  directory, create a new Python file for your agent. For example, my_agent.py:

```bash
touch agents/my_agent.py
```

Open agent/my_agent.py and implement your agent by subclassing Agent from agentserve:

```python
# agents/my_agent.py
from agentserve import Agent

class MyAgent(Agent):
    def process(self, task_data):
        # Implement your agent's logic here
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": task_data}]
        )
        return response.choices[0].message.content
```

#### 5. Create or Update Your main.py

In the root of your project, create a main.py file if it doesn't already exist:

```bash
touch main.py
```

Open main.py and set up the AgentServer:

```python
from agentserve import AgentServer
from agents.my_agent import MyAgent

agent_server = AgentServer(MyAgent)
app = agent_server.app
```

#### 6. Build and Run the Server

```bash
agentserve build
agentserve run
```

## Hosting

INSTRUCTIONS COMING SOON

## ROADMAP

- [ ] Add support for streaming responses
- [ ] Add easy instructions for more hosting options (GCP, Azure, AWS, etc.)
- [ ] Add support for multi model agents
- [ ] Add support for more agent frameworks

## License

This project is licensed under the MIT License.

## Contact

For any questions or issues, please contact Peter at peter@getprops.ai.
