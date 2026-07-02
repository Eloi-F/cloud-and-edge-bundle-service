FROM python:3.14-slim

WORKDIR /pic_identification

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY main.py .
COPY identification.py .

CMD ["python", "main.py"]
