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
        
        # FastAPI configuration
        fastapi_config = config.setdefault('fastapi', {})
        # CORS configuration within FastAPI config
        cors_config = fastapi_config.setdefault('cors', {})
        cors_origins_env = os.getenv('AGENTSERVE_CORS_ORIGINS')
        if cors_origins_env:
            cors_config['allow_origins'] = [origin.strip() for origin in cors_origins_env.split(',')]
        else:
            cors_config.setdefault('allow_origins', ["*"])

        cors_config['allow_credentials'] = self._get_bool_env(
            'AGENTSERVE_CORS_ALLOW_CREDENTIALS',
            cors_config.get('allow_credentials', True)
        )
        cors_methods_env = os.getenv('AGENTSERVE_CORS_ALLOW_METHODS')
        if cors_methods_env:
            cors_config['allow_methods'] = [method.strip() for method in cors_methods_env.split(',')]
        else:
            cors_config.setdefault('allow_methods', ["*"])

        cors_headers_env = os.getenv('AGENTSERVE_CORS_ALLOW_HEADERS')
        if cors_headers_env:
            cors_config['allow_headers'] = [header.strip() for header in cors_headers_env.split(',')]
        else:
            cors_config.setdefault('allow_headers', ["*"])

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
                
        queue_config = config.setdefault('queue', {})
        queue_config['max_workers'] = int(os.getenv('AGENTSERVE_QUEUE_MAX_WORKERS', queue_config.get('max_workers', 10)))

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
    
    def _get_bool_env(self, env_var, default):
        val = os.getenv(env_var)
        if val is not None:
            return val.lower() in ('true', '1', 'yes')
        return default