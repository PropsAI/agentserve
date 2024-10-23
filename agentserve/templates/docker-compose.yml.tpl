# docker-compose.yml

version: '3.8'

services:
  redis:
    image: redis:6.2
    ports:
      - '6379:6379'
    restart: always

  api_server:
    build: .
    command: uvicorn main:app --host 0.0.0.0 --port 8000
    environment:
      - REDIS_HOST=redis
    depends_on:
      - redis
    ports:
      - '8000:8000'
    restart: always

  worker:
    build: .
    command: python -m agentserve.cli worker
    environment:
      - REDIS_HOST=redis
    depends_on:
      - redis
    restart: always
