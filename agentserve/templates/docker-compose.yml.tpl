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
    command: uvicorn main:app --host 0.0.0.0 --port 5618
    environment:
      - REDIS_HOST=redis
    env_file:
      - .env
    depends_on:
      - redis
    ports:
      - '5618:5618'
    restart: always

  worker:
    build: .
    command: python -m agentserve.worker
    environment:
      - REDIS_HOST=redis
    depends_on:
      - redis
    restart: always
