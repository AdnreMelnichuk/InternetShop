FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir psycopg2-binary==2.9.9

COPY data_generator.py .

CMD ["python", "-u", "data_generator.py"]
