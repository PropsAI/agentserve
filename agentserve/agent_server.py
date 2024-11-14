# agentserve/agent_server.py

from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from .queues.task_queue import TaskQueue
from .agent_registry import AgentRegistry
from typing import Dict, Any, Optional
from .config import Config
from .logging_config import setup_logger
import uuid

class AgentServer:
    def __init__(self, config: Optional[Config] = None):
        self.logger = setup_logger("agentserve.server")
        self.app = FastAPI(debug=True)
        self.agent_registry = AgentRegistry()
        self.config = config or Config()
        self.task_queue = self._initialize_task_queue()
        self.agent = self.agent_registry.register_agent
        self._setup_routes()
        self.logger.info("AgentServer initialized")
    
    def _initialize_task_queue(self):
        task_queue_type = self.config.get('task_queue', 'local').lower()
        self.logger.info(f"Initializing {task_queue_type} task queue")
        
        try:
            if task_queue_type == 'celery':
                from .queues.celery_task_queue import CeleryTaskQueue
                return CeleryTaskQueue(self.config)
            elif task_queue_type == 'redis':
                from .queues.redis_task_queue import RedisTaskQueue
                return RedisTaskQueue(self.config)
            else:
                from .queues.local_task_queue import LocalTaskQueue
                return LocalTaskQueue(self.config)
        except Exception as e:
            self.logger.error(f"Failed to initialize task queue: {str(e)}")
            raise
    
    def _setup_routes(self):
        @self.app.post("/task/sync")
        async def sync_task(task_data: Dict[str, Any]):
            self.logger.debug(f"sync_task called with data: {task_data}")
            try:
                agent_function = self.agent_registry.get_agent()
                if getattr(agent_function, '_is_async', False):
                    self.logger.info("Function is async, running in event loop")
                    result = await agent_function(task_data)
                else:
                    self.logger.info("Function is sync, running directly")
                    result = agent_function(task_data)
                return {"result": result}
            except ValidationError as ve:
                if hasattr(ve, 'errors'):
                    raise HTTPException(
                        status_code=400,
                        detail={
                            "message": "Validation error",
                            "errors": ve.errors()
                        }
                    )
                raise HTTPException(status_code=400, detail=str(ve))
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/task/async")
        async def async_task(task_data: Dict[str, Any]):
            task_id = str(uuid.uuid4())
            agent_function = self.agent_registry.get_agent()
            self.task_queue.enqueue(agent_function, task_data, task_id)
            return {"task_id": task_id}

        @self.app.get("/task/status/{task_id}")
        async def get_status(task_id: str):
            status = self.task_queue.get_status(task_id)
            if status == 'not_found':
                raise HTTPException(status_code=404, detail="Task not found")
            return {"status": status}

        @self.app.get("/task/result/{task_id}")
        async def get_result(task_id: str):
            try:
                result = self.task_queue.get_result(task_id)
                if result is not None:
                    return {"result": result}
                else:
                    status = self.task_queue.get_status(task_id)
                    return {"status": status}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
    
    def run(self, host="0.0.0.0", port=8000):
        import uvicorn
        uvicorn.run(self.app, host=host, port=port)