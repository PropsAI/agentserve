# Dockerfile

FROM python:3.9-slim

# Environment variables to prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 5618

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5618"]
