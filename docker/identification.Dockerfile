FROM python:3.14-slim

WORKDIR /pic_identification

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY src/cloud/picture_identification/ .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
        --index-url https://download.pytorch.org/whl/cpu \
        torch torchvision && \
    pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]