import logging
import sys
from typing import Optional

def setup_logger(name: str = "agentserve", level: Optional[str] = None) -> logging.Logger:
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    log_level = getattr(logging, (level or "DEBUG").upper())
    logger.setLevel(log_level)
    
    return logger