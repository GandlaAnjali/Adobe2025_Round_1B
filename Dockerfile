# Base image - lightweight & amd64 compatible
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary folders
RUN mkdir -p /app/input /app/output

# Run the main script when the container starts
CMD ["python", "run.py"]
