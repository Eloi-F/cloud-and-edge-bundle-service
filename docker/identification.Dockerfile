FROM python:3.14-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

COPY src/picture_identification/ ./src/picture_identification/
COPY src/models/ ./src/models/
COPY src/odrl/ ./src/odrl/
COPY src/logging/ ./src/logging/

COPY src/picture_identification/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
        --index-url https://download.pytorch.org/whl/cpu \
        torch torchvision && \
    pip install --no-cache-dir -r /tmp/requirements.txt

CMD ["uvicorn", "src.picture_identification.main:app", "--host", "0.0.0.0"]