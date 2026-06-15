FROM python:3.10-slim-buster

WORKDIR /app

COPY . .

RUN apt-get update -y && \
    apt-get install -y awscli

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "app.py"]