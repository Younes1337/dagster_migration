FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install dagster dagit dagster-postgres \
    && pip install .

# Expose Dagit port
EXPOSE 3000

# Default command (can be overridden in docker-compose)
CMD ["dagit", "-h", "0.0.0.0", "-p", "3000"]
