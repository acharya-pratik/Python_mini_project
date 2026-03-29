FROM python:3.11-slim

WORKDIR /app

# Install minimal system dependencies
# libgomp1 is needed for some scikit-learn/numpy operations (OpenMP)
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Cache requirements installation
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the necessary code (respecting .dockerignore)
COPY . .

# Ensure required directories exist for simulation and logs
RUN mkdir -p data/processed data/simulation/chunks member3_ml/models logs

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Default port for Streamlit
EXPOSE 8501

# The command is usually overridden in docker-compose for dev, 
# but this is a solid production-ready default.
CMD ["streamlit", "run", "member4/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
