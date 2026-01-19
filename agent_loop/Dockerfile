FROM python:3.11-slim
WORKDIR /app
COPY .. /app
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements-dev.txt
CMD ["python", "-m", "agent_loop.orchestrator"]
