FROM python:3.14-slim

WORKDIR /decision

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY main.py .
COPY speed_decision.py .

CMD ["python", "main.py"]
