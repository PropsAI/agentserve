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
![Beta](https://img.shields.io/badge/Status-Beta-yellow)


AgentServe is an lightweight framework for hosting and scaling AI agents. It is designed to be easy to use and integrate with existing projects and agent / LLM frameworks. It wraps your agent in a REST API and supports optional task queuing for scalability.

## Goals and Objectives

The goal of AgentServe is to provide the easiest way to take an local agent to production and standardize the communication layer between multiple agents, humans, and other systems.

## Features

- **Standardized:** AgentServe provides a standardized way to communicate with AI agents via a REST API.
- **Framework Agnostic:** AgentServe supports multiple agent frameworks (OpenAI, LangChain, LlamaIndex, and Blank).
- **Task Queuing:** AgentServe supports optional task queuing for scalability. Choose between local, Redis, or Celery task queues based on your needs.
- **Configurable:** AgentServe is designed to be configurable via an `agentserve.yaml` file and overridable with environment variables.
- **Easy to Use:** AgentServe aims to be easy to use and integrate with existing projects and make deployment as simple as possible.

## Requirements

- Python 3.9+

## Installation

To install AgentServe, you can use pip:

```bash
pip install -U agentserve
```

## Getting Started

AgentServe allows you to easily wrap your agent code in a FastAPI application and expose it via REST endpoints. Below are the steps to integrate AgentServe into your project.

### 1. Install AgentServe

First, install the `agentserve` package using pip:

```bash
pip install -U agentserve
```

Make sure your virtual environment is activated if you're using one.


### 2. Create or Update Your Agent

Within your entry point file (e.g. `main.py`) we will import `agentserve` and create an app instance, then decorate an agent function with `@app.agent`. Finally, we will call `app.run()` to start the server.

The agent function should take a single argument, `task_data`, which will be a dictionary of data prequired by your agent.

**Example:**

```python
# main.py
import agentserve
from openai import OpenAI

app = agentserve.app()

@app.agent
def my_agent(task_data):
    # Your agent logic goes here
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": task_data["prompt"]}]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    app.run()
```

In this example:
- We import agentserve and create an app instance using `agentserve.app()`.
- We define our agent function `my_agent` and decorate it with `@app.agent`.
- Within the agent function, we implement our agent's logic.
- We call `app.run()` to start the server.

### 3. Run the Agent Server

To run the agent server, use the following command:

```bash
python main.py
```

### 4. Configure Task Queue (Optional)

By default, AgentServe uses a local task queue, which is suitable for development and testing. If you need more robust queue management for production, you can configure AgentServe to use Redis or Celery.

**Using a Configuration File**
Create a file named agentserve.yaml in your project directory:

```yaml
# agentserve.yaml

task_queue: celery  # Options: 'local', 'redis', 'celery'

celery:
  broker_url: pyamqp://guest@localhost//
```

**Using Environment Variables**

Alternatively, you can set configuration options using environment variables:

```bash
export AGENTSERVE_TASK_QUEUE=celery
export AGENTSERVE_CELERY_BROKER_URL=pyamqp://guest@localhost//
```

### 5. Start the Worker (if using Celery or Redis)

To start the worker, use the following command:

```bash
agentserve startworker
```

### 6. Test the Agent

With the server and worker (if needed) running, you can test your agent using the available endpoints.

**Synchronous Task Processing**

`POST /task/sync`

```bash
curl -X POST http://localhost:8000/task/sync \
     -H "Content-Type: application/json" \
       -d '{"input": "Test input"}'
```
**Asynchronously process a task**

`POST /task/async`

```bash
curl -X POST http://localhost:8000/task/async \
     -H "Content-Type: application/json" \
       -d '{"input": "Test input"}'
```

**Get the status of a task**

`GET /task/status/:task_id`

```bash
curl http://localhost:8000/task/status/1234567890
```

**Get the result of a task**

`GET /task/result/:task_id`

```bash
curl http://localhost:8000/task/result/1234567890
```

## Configuration Options

AgentServe allows you to configure various aspects of the application using a configuration file or environment variables.

#### Using agentserve.yaml 

Place an `agentserve.yaml` file in your project directory with the desired configurations.

**Example:**

```yaml
# agentserve.yaml

task_queue: celery  # Options: 'local', 'redis', 'celery'

celery:
  broker_url: pyamqp://guest@localhost//

redis:
  host: localhost
  port: 6379

server:
  host: 0.0.0.0
  port: 8000
```

#### Using Environment Variables

Set the desired configuration options using environment variables.

You can override configurations using environment variables without modifying the configuration file.

- `AGENTSERVE_TASK_QUEUE`
- `AGENTSERVE_CELERY_BROKER_URL`
- `AGENTSERVE_REDIS_HOST`
- `AGENTSERVE_REDIS_PORT`
- `AGENTSERVE_SERVER_HOST`
- `AGENTSERVE_SERVER_PORT`

**Example:**

```bash
export AGENTSERVE_TASK_QUEUE=redis
export AGENTSERVE_REDIS_HOST=redis-server-host
export AGENTSERVE_REDIS_PORT=6379
```

## Advanced Usage

### Integrating with Existing Projects

You can integrate AgentServe into your existing projects by importing agentserve and defining your agent function.

**Example:**

```python
# main.py
import agentserve

app = agentserve.app()

@app.agent
def my_custom_agent(task_data):
    # Your custom agent logic (e.g. using LangChain, LlamaIndex, etc.)
    result = perform_complex_computation(task_data)
    return {"result": result}

if __name__ == "__main__":
    app.run()
```

### Input Validation

AgentServe allows you to validate the input to your agent function using Pydantic. Simply add an input schema to your agent function.

**Example:**

```python
# main.py
import agentserve
from pydantic import BaseModel

class MyInputSchema(BaseModel):
    prompt: str

@app.agent(input_schema=MyInputSchema)
def my_custom_agent(task_data):
    # Your custom agent logic
    return {"result": "Hello, world!"}

if __name__ == "__main__":
    app.run()
```

## Hosting

INSTRUCTIONS COMING SOON

## ROADMAP

- [ ] Add support for streaming responses
- [ ] Add easy instructions for more hosting options (GCP, Azure, AWS, etc.)
- [ ] Add support for external storage for task results
- [ ] Add support for multi model agents
- [ ] Add support for more agent frameworks

## License

This project is licensed under the MIT License.

## Contact

For any questions or issues, please contact Peter at peter@getprops.ai.