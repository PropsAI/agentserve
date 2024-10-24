# agentserve/cli.py

import click
import os
import shutil
from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent / 'templates'

# Mapping of framework choices to their respective agent import and class names
FRAMEWORKS = {
    'openai': {
        'agent_import': 'from agents.example_openai_agent import ExampleAgent',
        'agent_class': 'ExampleAgent',
        'agent_template_filename': 'example_openai_agent.py.tpl'
    },
    'langchain': {
        'agent_import': 'from agents.example_langchain_agent import ExampleAgent',
        'agent_class': 'ExampleAgent',
        'agent_template_filename': 'example_langchain_agent.py.tpl'
    },
    'llama': {
        'agent_import': 'from agents.example_llama_agent import ExampleAgent',
        'agent_class': 'ExampleAgent',
        'agent_template_filename': 'example_llamaindex_agent.py.tpl'
    },
    'blank': {
        'agent_import': 'from agents.example_agent import ExampleAgent',
        'agent_class': 'ExampleAgent',
        'agent_template_filename': 'example_agent.py.tpl'
    }
}

@click.group()
def main():
    """CLI tool for managing AI agents."""
    click.echo(click.style("\nWelcome to AgentServe CLI\n\n", fg='green', bold=True))
    click.echo("Go to https://github.com/Props/agentserve for more information.\n\n\n")

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

    # Define the list of target directories to be created
    target_dirs = ['agent'] 

    # Create project directory
    project_path.mkdir()

    # Create subdirectories
    for dir_name in target_dirs:
        (project_path / dir_name).mkdir()

    # Copy and process main.py template
    main_tpl_path = TEMPLATES_DIR / 'main.py.tpl'
    with open(main_tpl_path, 'r') as tpl_file:
        main_content = tpl_file.read()

    agent_import = FRAMEWORKS[framework]['agent_import']
    agent_class = FRAMEWORKS[framework]['agent_class']
    main_content = main_content.replace('{{AGENT_IMPORT}}', agent_import)
    main_content = main_content.replace('{{AGENT_CLASS}}', agent_class)

    main_dst_path = project_path / 'main.py'
    with open(main_dst_path, 'w') as dst_file:
        dst_file.write(main_content)

    # Copy agent template to agents directory
    agent_template_filename = FRAMEWORKS[framework]['agent_template_filename']
    agent_src_path = TEMPLATES_DIR / 'agents' / agent_template_filename
    agent_dst_path = project_path / 'agents' / agent_template_filename[:-4]  # Remove '.tpl' extension
    shutil.copyfile(agent_src_path, agent_dst_path)

    # Copy .env template
    env_tpl_path = TEMPLATES_DIR / '.env.tpl'
    env_dst_path = project_path / '.env'
    shutil.copyfile(env_tpl_path, env_dst_path)

    # Create requirements.txt
    requirements_path = project_path / 'requirements.txt'
    with open(requirements_path, 'w') as f:
        f.write('agentserve\n')
        if framework == 'openai':
            f.write('openai\n')
        elif framework == 'langchain':
            f.write('langchain\n')
        elif framework == 'llama':
            f.write('llama-index\n')

    click.echo(f"Initialized new agent project at '{project_path}' with '{framework}' framework.")
    click.echo(f"    - Now run 'cd {project_name}'")
    click.echo("    - Update the .env file with your API keys and other environment variables")
    click.echo("    - To generate Dockerfiles, run 'agentserve build'")
    click.echo("    - Then run 'agentserve run' to start the API server and worker.")

@main.command()
def build():
    """Generate Dockerfiles."""
    project_path = Path.cwd()
    docker_dir = project_path / 'docker'
    docker_dir.mkdir(exist_ok=True)

    templates = {
        'Dockerfile.tpl': 'Dockerfile',
        'docker-compose.yml.tpl': 'docker-compose.yml'
    }

    for tpl_name, dst_name in templates.items():
        src_path = TEMPLATES_DIR / tpl_name
        dst_path = docker_dir / dst_name
        shutil.copyfile(src_path, dst_path)

    click.echo(f"Dockerfiles have been generated in '{docker_dir}'.")

@main.command()
def run():
    """Run the API server and worker."""
    docker_dir = Path.cwd() / 'docker'
    if not docker_dir.exists():
        click.echo("Docker directory not found. Please run 'agentserve build' first.")
        return
    os.chdir(docker_dir)
    os.system('docker-compose up --build')

if __name__ == '__main__':
    main()
