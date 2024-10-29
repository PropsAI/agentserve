# agentserve/config.py

import os
import yaml

class Config:
    def __init__(self):
        self.config = self._load_config()

    def _load_config(self):
        # Load from 'agentserve.yaml' if exists
        config_path = 'agentserve.yaml'
        config = {}
        if os.path.exists(config_path):
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file) or {}

        # Override with environment variables
        config['task_queue'] = os.getenv('AGENTSERVE_TASK_QUEUE', config.get('task_queue', 'local'))

        # Celery configuration
        celery_broker_url = os.getenv('AGENTSERVE_CELERY_BROKER_URL')
        if celery_broker_url:
            config.setdefault('celery', {})['broker_url'] = celery_broker_url

        # Redis configuration
        redis_host = os.getenv('AGENTSERVE_REDIS_HOST')
        redis_port = os.getenv('AGENTSERVE_REDIS_PORT')
        if redis_host or redis_port:
            redis_config = config.setdefault('redis', {})
            if redis_host:
                redis_config['host'] = redis_host
            if redis_port:
                redis_config['port'] = int(redis_port)

        # Server configuration
        server_host = os.getenv('AGENTSERVE_SERVER_HOST')
        server_port = os.getenv('AGENTSERVE_SERVER_PORT')
        if server_host or server_port:
            server_config = config.setdefault('server', {})
            if server_host:
                server_config['host'] = server_host
            if server_port:
                server_config['port'] = int(server_port)

        return config

    def get(self, key, default=None):
        return self.config.get(key, default)

    def get_nested(self, *keys, default=None):
        value = self.config
        for key in keys:
            if not isinstance(value, dict):
                return default
            value = value.get(key)
            if value is None:
                return default
        return value