<!-- IMAGE -->


# AgentServe SDK

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

AgentServe provides a Command-Line Interface (CLI) tool to manage your AI agent projects. Below are the available commands and their usages.

```bash
agentserve init <project_name> [--framework <framework>] # Initialize a new project
agentserve setup # Add AgentServe to an existing project
```

More detailed information about each command is provided below

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

### Run the Server

Use Docker Compose to build and run the server:

   ```bash
   docker-compose up --build
   ```

This command starts the API server and a Redis instance, allowing your agent to process tasks.

### Test the Agent

The agent will be running on `http://localhost:8000/` and have the following endpoint:



## Example Project Structure

After initializing a new project, your project directory will look like this:

```
my_project/
├── Dockerfile
├── docker-compose.yml
├── main.py
├── example_agent.py
├── requirements.txt
```

- **`main.py`**: The main application file where the agent server is configured.
- **`Dockerfile` & `docker-compose.yml`**: Docker configurations for building and running the application.
- **`example_openai_agent.py`**: An example agent tailored to the OpenAI framework.
- **`requirements.txt`**: Lists Python dependencies.

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

### Setup Command (for existing projects)

Navigate to your existing project directory and run:

```bash
agentserve setup
```

**Result:**

- Adds AgentServe to the project and sets up the necessary files.
- Note this command will not run if the project already included a main.py, Dockerfile or docker-compose.yml

## Customization

Depending on the chosen framework, you can customize the example agent to fit your specific needs:

- **OpenAI**: Modify `example_openai_agent.py` to implement OpenAI-specific functionalities.
- **LangChain**: Customize `example_langchain_agent.py` for LangChain integrations.
- **Llama Index**: Adjust `example_llama_agent.py` for Llama Index operations.
- **Blank**: Implement your own agent by creating a new class that inherits from the `Agent` class and implements the `process` method.

## License

This project is licensed under the MIT License.

## Contact

For any questions or issues, please contact Peter at peter@getprops.ai.