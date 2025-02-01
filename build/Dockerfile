FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY build/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app/ app/

# Expose the FastAPI default port
EXPOSE 8000

# Set the command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
