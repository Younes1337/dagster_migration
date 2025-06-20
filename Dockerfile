FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy requirements first and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Now copy the rest of your code
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install dagster dagit dagster-postgres \
    && pip install .

# Expose Dagit port
EXPOSE 3000

# Default command (can be overridden in docker-compose)
CMD ["dagit", "-h", "0.0.0.0", "-p", "3000"]
