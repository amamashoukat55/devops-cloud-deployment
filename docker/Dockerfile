
FROM python:3.12-slim

WORKDIR /app

COPY app/app.py .

RUN pip install --no-cache-dir Flask "psycopg[binary]"

EXPOSE 8000

CMD ["python", "app.py"]
