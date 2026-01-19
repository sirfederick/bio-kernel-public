FROM python:3.11-slim
WORKDIR /app
COPY .. /app
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements-dev.txt
CMD ["uvicorn", "dashboard.realtime_dashboard:RealTimeDashboard().app", "--host", "0.0.0.0", "--port", "8000"]
