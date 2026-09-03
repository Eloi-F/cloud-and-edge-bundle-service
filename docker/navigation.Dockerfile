FROM python:3.14-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

COPY src/navigation/ ./src/navigation/
COPY src/models/ ./src/models/
COPY src/odrl/ ./src/odrl/
COPY src/logging_config/ ./src/logging_config/

COPY src/navigation/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt


CMD ["uvicorn", "src.navigation.main:app", "--host", "0.0.0.0"]