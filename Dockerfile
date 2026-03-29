FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for MySQL client
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Environment variables
ENV PYTHONUNBUFFERED=1

# Expose Streamlit port
EXPOSE 8501

# Default command (can be overridden in docker-compose)
CMD ["streamlit", "run", "member4/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
