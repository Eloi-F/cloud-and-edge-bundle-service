FROM python:3.14-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# The local client is self-contained (flat imports: core.*, services.*,
# odrl_eval.*), so only src/local is needed.
COPY src/local/ ./src/local/

COPY src/local/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt

CMD ["python", "src/local/main.py"]
