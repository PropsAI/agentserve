```
   ___                __  ____
  / _ |___ ____ ___  / /_/ __/__ _____  _____
 / __ / _ `/ -_) _ \/ __/\ \/ -_) __/ |/ / -_)
/_/ |_\_, /\__/_//_/\__/___/\__/_/  |___/\__/
     /___/
```

# AgentServe SDK

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![PyPI Version](https://img.shields.io/pypi/v/agentserve.svg)

AgentServe is an SDK & CLI for hosting and managing AI agents. It provides a simple interface to wrap your agent in a FastAPI server with a Redis queue to maintain tasks. The output is a single docker image that you can deploy anywhere.

## Goals and Objectives

The goal of AgentServe is to provide the easiest way to take an local agent to production and standardize the communication layer between multiple agents, humans, and other systems.

## Features

- **Standardized:** AgentServe provides a standardized way to communicate with AI agents via a REST API.
- **Framework Agnostic:** AgentServe supports multiple agent frameworks (OpenAI, LangChain, LlamaIndex, and Blank).
- **Dockerized:** The output is a single docker image that you can deploy anywhere.
- **Easy to Use:** AgentServe provides a CLI tool to initialize and setup your AI agent projects.

## Requirements

- Python 3.9+

## Installation

To install the AgentServe SDK, you can use pip:

```bash
pip install agentserve
```

## CLI Commands

AgentServe provides a Command-Line Interface (CLI) tool to setup your AI agent projects. Below are the available commands and their usages.

```bash
agentserve init <project_name> [--framework <framework>] # Initialize a new project
agentserve build # Generate Dockerfiles
agentserve run # Run the API server and worker
```

## Getting Started

First we need to set up agentserve in our project. We can do this by running the `init` command to create a new project or by running the `setup` command to add AgentServe to an existing project.

### Initialize a New Project

Create a new AgentServe project with a specified agent framework.

**Command:**

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
agentserve init my_project --framework openai
```

This command adds AgentServe to the current project using the OpenAI framework.

### Update Environment Variables

You can update the environment variables in the `.env` file to add your OpenAI API key, or any other variables you need.

### Run the Server

Use Docker Compose to build and run the server:

```bash
docker-compose up --build
```

This command starts the API server and a Redis instance, allowing your agent to process tasks.

### Test the Agent

The agent will be running on `http://localhost:8000/` and have the following endpoint:

- `POST /task/sync` - Synchronously process a task
- `POST /task/async` - Asynchronously process a task
- `GET /task/status/:task_id` - Get the status of a task
- `GET /task/result/:task_id` - Get the result of a task

**Example:**

```bash
curl -X POST http://localhost:8000/task/sync -H "Content-Type: application/json" -d '{"prompt": "What is the capital of France?"}'
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

## CLI Usage

### Init Command (for new projects)

To create a new project with AgentServe:

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

## License

This project is licensed under the MIT License.

## Contact

For any questions or issues, please contact Peter at peter@getprops.ai.
