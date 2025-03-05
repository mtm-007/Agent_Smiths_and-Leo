FROM python:3.12.8-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

COPY .env .env

CMD ["python", "src/meeting_minutes/main.py"]
