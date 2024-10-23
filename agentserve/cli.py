# agentserve/cli.py

import click
import os
import shutil
from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent / 'templates'

# Mapping of framework choices to their respective agent import and class names
FRAMEWORKS = {
    'openai': {
        'agent_import': 'from example_openai_agent import OpenAIAgent  # Replace with your OpenAI agent class name',
        'agent_class': 'OpenAIAgent',
        'agent_template_filename': 'example_openai_agent.py.tpl'
    },
    'langchain': {
        'agent_import': 'from example_langchain_agent import LangChainAgent  # Replace with your LangChain agent class name',
        'agent_class': 'LangChainAgent',
        'agent_template_filename': 'example_langchain_agent.py.tpl'
    },
    'llama': {
        'agent_import': 'from example_llama_agent import LlamaIndexAgent  # Replace with your Llama Index agent class name',
        'agent_class': 'LlamaIndexAgent',
        'agent_template_filename': 'example_llamaindex_agent.py.tpl'
    },
    'blank': {
        'agent_import': 'from example_agent import ExampleAgent  # Replace with your agent class name',
        'agent_class': 'ExampleAgent',
        'agent_template_filename': 'example_agent.py.tpl'
    }
}

@click.group()
def main():
    """CLI tool for managing AI agents."""
    click.echo("Welcome to AgentServe CLI\n")
    click.echo("Type 'agentserve init <project_name> [--framework <framework>]' to start a new project.\n")
    click.echo("Type 'agentserve add [--framework <framework>]' to add AgentServe to an existing project.\n")
    click.echo("Available frameworks: openai, langchain, llama")
    click.echo("Go to https://github.com/Props/agentserve for more information.\n")

@main.command()
@click.argument('project_name')
@click.option('--framework', type=click.Choice(FRAMEWORKS.keys()), default='openai', help='Type of agent framework to use.')
def init(project_name, framework):
    """Initialize a new agent project."""
    project_path = Path.cwd() / project_name

    # Check if the project directory already exists
    if project_path.exists():
        click.echo(f"Directory '{project_name}' already exists.")
        return

    # Define the list of target files to be created
    target_files = ['main.py', 'Dockerfile', 'docker-compose.yml', 'requirements.txt']

    # Check if any of the target files already exist in the current directory
    existing_files = [file for file in target_files if (project_path / file).exists()]
    if existing_files:
        click.echo(
            f"Initialization aborted. The following files already exist in '{project_name}': "
            f"{', '.join(existing_files)}"
        )
        return

    # Create project directory
    project_path.mkdir()

    # Copy and process main.py template
    main_tpl_path = TEMPLATES_DIR / 'main.py.tpl'
    with open(main_tpl_path, 'r') as tpl_file:
        main_content = tpl_file.read()

    agent_import = FRAMEWORKS[framework]['agent_import']
    agent_class = FRAMEWORKS[framework]['agent_class']
    agent_template_filename = FRAMEWORKS[framework]['agent_template_filename']

    main_content = main_content.replace('{{AGENT_IMPORT}}', agent_import)
    main_content = main_content.replace('{{AGENT_CLASS}}', agent_class)

    main_dst_path = project_path / 'main.py'
    with open(main_dst_path, 'w') as dst_file:
        dst_file.write(main_content)

    # Copy other template files
    for template_name in ['Dockerfile.tpl', 'docker-compose.yml.tpl']:
        src_path = TEMPLATES_DIR / template_name
        dst_file_name = template_name[:-4]  # Remove '.tpl' extension
        dst_path = project_path / dst_file_name
        shutil.copyfile(src_path, dst_path)

    # Handle agent example file based on chosen framework
    agent_template_filename = FRAMEWORKS[framework]['agent_template_filename']
    agent_src_path = TEMPLATES_DIR / "agents" /  agent_template_filename
    agent_dst_path = project_path / agent_template_filename.replace('.tpl', '.py')
    shutil.copyfile(agent_src_path, agent_dst_path)

    # Update requirements.txt
    requirements_path = project_path / 'requirements.txt'
    with open(requirements_path, 'w') as f:
        f.write('agentserve\n')
        if framework == 'openai':
            f.write('openai\n')
        elif framework == 'langchain':
            f.write('langchain\n')
        elif framework == 'llamaindex':
            f.write('llama-index\n')
        elif framework == 'blank':
            pass

    # Create .env file
    env_path = project_path / '.env'
    with open(env_path, 'w') as f:
        if framework == 'openai':
            f.write('OPENAI_API_KEY=<your-openai-api-key>\n')
        elif framework == 'langchain':
            f.write('OPENAI_API_KEY=<your-openai-api-key>\n')
        elif framework == 'llamaindex':
            f.write('OPENAI_API_KEY=<your-openai-api-key>\n')
        elif framework == 'blank':
            pass

    click.echo(f"Initialized new agent project at '{project_path}' with '{framework}' framework.")

@main.command()
def setup():
    """Add AgentServe to an existing project."""
    project_path = Path.cwd()

    # List of files to add
    files_to_add = ['main.py', 'Dockerfile', 'docker-compose.yml', 'requirements.txt']

    # Check if AgentServe is already initialized
    existing_files = [file for file in files_to_add if (project_path / file).exists()]
    if existing_files:
        click.echo(
            f"AgentServe files already exist in the current directory: {', '.join(existing_files)}. Please remove or rename them before adding AgentServe again."
        )
        return

    # Copy templates to the project directory
    for template_name in ['main.py.tpl', 'Dockerfile.tpl', 'docker-compose.yml.tpl']:
        src_path = TEMPLATES_DIR / template_name
        dst_path = project_path / template_name[:-4]  # Remove '.tpl' extension
        shutil.copyfile(src_path, dst_path)

    # Append 'agentserve' to requirements.txt or create it if it doesn't exist
    requirements_path = project_path / 'requirements.txt'
    if requirements_path.exists():
        with open(requirements_path, 'a') as f:
            f.write('\nagentserve\n')
    else:
        with open(requirements_path, 'w') as f:
            f.write('agentserve\n')

    click.echo(f"AgentServe has been added to the project at '{project_path}'.")

if __name__ == '__main__':
    main()
