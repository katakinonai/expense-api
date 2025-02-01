# Base image for production
FROM python:3.11-slim as base

WORKDIR /app

# Install production dependencies
COPY build/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ app/

EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Linting stage for CI
FROM base as lint

# Install development dependencies for linting
COPY build/requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

# Copy the application code
COPY app/ app/

# Copy the python-lint.sh script into the root directory of the container
COPY python-lint.sh /python-lint.sh

# Make the script executable
RUN chmod +x /python-lint.sh

# Run the python-lint.sh script when the container starts
CMD ["sh", "/python-lint.sh", "."]
