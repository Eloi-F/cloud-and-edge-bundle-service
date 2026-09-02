FROM python:3.14-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

COPY src/image_compression/ ./src/image_compression/
COPY src/models/ ./src/models/
COPY src/odrl/ ./src/odrl/
COPY src/logging/ ./src/logging/

COPY src/image_compression/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt


CMD ["uvicorn", "src.image_compression.main:app", "--host", "0.0.0.0"]