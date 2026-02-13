FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONPATH=/app:/workspace/swir_library
CMD ["celery", "-A", "tasks.celery_app", "worker", "--loglevel=info"]
