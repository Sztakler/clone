FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY .env /app/.env

COPY . .

EXPOSE 5487

CMD ["python", "app/main.py"]
