# agentserve/agent_server.py

from fastapi import FastAPI, HTTPException
from typing import Dict, Any
from rq import Queue
from redis import Redis
import uuid
import os

class AgentServer:
    def __init__(self, agent_class: type):
        self.agent = agent_class()
        self.app = FastAPI()
        self.redis_conn = Redis(host=os.getenv('REDIS_HOST', 'redis'), port=6379)
        self.task_queue = Queue(connection=self.redis_conn)
        self._setup_routes()

    def _setup_routes(self):
        @self.app.post("/task/sync")
        async def sync_task(task_data: Dict[str, Any]):
            try:
                result = self.agent.process(task_data)
                return {"result": result}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/task/async")
        async def async_task(task_data: Dict[str, Any]):
            task_id = str(uuid.uuid4())
            job = self.task_queue.enqueue(self.agent.process, task_data, job_id=task_id)
            return {"task_id": task_id}

        @self.app.get("/task/status/{task_id}")
        async def get_status(task_id: str):
            job = self.task_queue.fetch_job(task_id)
            if job:
                return {"status": job.get_status()}
            else:
                raise HTTPException(status_code=404, detail="Task not found")

        @self.app.get("/task/result/{task_id}")
        async def get_result(task_id: str):
            job = self.task_queue.fetch_job(task_id)
            if job:
                if job.is_finished:
                    return {"result": job.result}
                elif job.is_failed:
                    return {"status": "failed", "error": str(job.exc_info)}
                else:
                    return {"status": job.get_status()}
            else:
                raise HTTPException(status_code=404, detail="Task not found")
