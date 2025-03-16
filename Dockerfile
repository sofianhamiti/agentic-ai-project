FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    less \
    groff \
    unzip \
    git \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install AWS CLI v2
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf aws awscliv2.zip

# Set working directory
WORKDIR /app

# Copy README.md and pyproject.toml for dependency installation
COPY README.md pyproject.toml ./
COPY requirements.txt ./

# Install the project in editable mode
RUN pip install --no-cache-dir -e .

# Install specific requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set Python path to include the app directory
ENV PYTHONPATH=/app

# Default command
CMD ["python", "-m", "src.main"]
