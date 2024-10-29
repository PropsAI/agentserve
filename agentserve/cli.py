# agentserve/cli.py

import click
from .config import Config

@click.group()
def main():
    """CLI tool for managing AI agents."""
    click.echo(click.style("\nWelcome to AgentServe CLI\n\n", fg='green', bold=True))
    click.echo("Go to https://github.com/Props/agentserve for more information.\n\n\n")

@cli.command()
def startworker():
    """Starts the AgentServe worker (if required)."""
    config = Config()
    task_queue_type = config.get('task_queue', 'local').lower()

    if task_queue_type == 'celery':
        from .queues.celery_task_queue import CeleryTaskQueue
        task_queue = CeleryTaskQueue(config)
        # Start the Celery worker
        argv = [
            'worker',
            '--loglevel=info',
            '--pool=solo',  # Use 'solo' pool to avoid issues on some platforms
        ]
        task_queue.celery_app.worker_main(argv)
    elif task_queue_type == 'redis':
        # For Redis (RQ), start a worker process
        from rq import Worker, Connection
        from .queues.redis_task_queue import RedisTaskQueue
        task_queue = RedisTaskQueue(config)
        with Connection(task_queue.redis_conn):
            worker = Worker([task_queue.task_queue])
            worker.work(log_level='INFO')
    else:
        click.echo("No worker required for the 'local' task queue.")
