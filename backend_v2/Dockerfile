FROM python:3.9-slim

WORKDIR /app

# Install system dependencies (for psycopg2 and other dependencies)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

EXPOSE 8000

CMD /wait-for-it.sh db:5432 -- sh -c 'python create_database.py && uvicorn backend:app --host 0.0.0.0 --port 8000 --reload --log-level debug'