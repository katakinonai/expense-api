FROM python:3.11-slim as base

WORKDIR /app

COPY build/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY app/ app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM base as lint

COPY build/requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY app/ app/
COPY tests/ /app/tests/

COPY pyproject.toml /app/pyproject.toml
COPY python-lint.sh /app/python-lint.sh

RUN chmod +x /app/python-lint.sh

CMD ["bash", "/app/python-lint.sh", "/app", "/app"]
