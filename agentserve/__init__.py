# agentserve/__init__.py
from .agent_server import AgentServer as app
from .logging_config import setup_logger

logger = setup_logger()