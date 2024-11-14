import logging
import sys
from typing import Optional

_loggers = {}

def setup_logger(name: str = "agentserve", level: Optional[str] = None) -> logging.Logger:
    if name in _loggers:
        return _loggers[name]
        
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False  # Prevent duplicate logging
    
    log_level = getattr(logging, (level or "DEBUG").upper())
    logger.setLevel(log_level)
    
    _loggers[name] = logger
    return logger