FROM python:3.14-slim

WORKDIR /navigation

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY main.py .
COPY trajectory.py .

CMD ["python", "main.py"]
