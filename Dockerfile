# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /ctf

# Install system dependencies
RUN apt-get update && \
    apt-get install -y wget nano git && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir flask pyyaml

# Clone the repository
RUN git clone https://github.com/bwithe/ctf .

# Set working directory to app
WORKDIR /ctf/app

# Expose port
EXPOSE 8000

# Start the application
CMD ["python", "main.py"]
