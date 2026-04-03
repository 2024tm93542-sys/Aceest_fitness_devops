# Minimal Flask app Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY app/ app
COPY tests/ tests
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "-m", "app.main"]
